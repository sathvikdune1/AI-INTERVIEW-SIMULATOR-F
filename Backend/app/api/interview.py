from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from bson import ObjectId
from datetime import datetime, timezone
from typing import Optional
import os, shutil

from Backend.app.services.resume_parser import analyze_resume
from Backend.app.services.dynamic_question_engine import generate_interview_questions
from Backend.app.services.gemini_answer_evaluator import evaluate_answer
from Backend.app.services.scoring_engine import calculate_final_score
from Backend.app.services.code_analyzer import analyze_code
from Backend.app.db.mongodb import interviews_collection

router = APIRouter(prefix="/api/interview", tags=["Interview"])

UPLOAD_DIR = "Backend/app/db/resumes"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# =================================================
# START INTERVIEW
# =================================================
@router.post("/start")
def start_interview(
    name: str = Form(None),
    full_name: str = Form(None),
    email: str = Form(...),
    mobile: str = Form(...),
    job_role: str = Form(...),
    difficulty: str = Form(...)
):
    final_name = name or full_name
    if not final_name:
        raise HTTPException(400, "Name required")

    interview = {
        "name": final_name,
        "email": email,
        "mobile": mobile,
        "job_role": job_role,
        "difficulty": difficulty,
        "created_at": datetime.now(timezone.utc),
        "current_index": 0,
        "answers": [],
        "resume_score": 0,
        "status": "started"
    }

    res = interviews_collection.insert_one(interview)
    return {"interview_id": str(res.inserted_id)}

# =================================================
# UPLOAD RESUME
# =================================================
@router.post("/upload-resume")
def upload_resume(
    interview_id: str = Form(...),
    resume: UploadFile = File(...)
):
    if not resume.filename.lower().endswith(".pdf"):
        raise HTTPException(400, "Only PDF resumes allowed")

    path = os.path.join(UPLOAD_DIR, resume.filename)
    with open(path, "wb") as f:
        shutil.copyfileobj(resume.file, f)

    analysis = analyze_resume(path)

    interviews_collection.update_one(
        {"_id": ObjectId(interview_id)},
        {"$set": {
            "resume_score": analysis["score"],
            "skills": analysis["skills"]
        }}
    )

    return {"message": "Resume uploaded"}

# =================================================
# GENERATE QUESTIONS (LOCKED ORDER)
# =================================================
@router.post("/generate-questions")
def generate_questions(interview_id: str = Form(...)):
    interview = interviews_collection.find_one({"_id": ObjectId(interview_id)})
    if not interview:
        raise HTTPException(404, "Interview not found")

    q = generate_interview_questions(
        resume_skills=interview.get("skills", []),
        job_role=interview["job_role"],
        difficulty=interview["difficulty"]
    )

    # ---------- SAFE NORMALIZATION ----------
    self_intro = q.get("self_intro", [])[:1] or [
        "Can you briefly introduce yourself and your experience relevant to this role?"
    ]

    technical = q.get("technical", [])[:6]
    while len(technical) < 6:
        technical.append(
            f"Explain a core concept related to {interview['job_role']}."
        )

    aptitude = q.get("aptitude", [])[:1] or [
        "If the probability of an event occurring is 0.25, what is the probability it does not occur?"
    ]

    coding = q.get("coding", [])[:2]
    while len(coding) < 2:
        coding.append(
            "Write a Python function that solves a basic real-world problem."
        )

    ordered_questions = (
        [{"text": self_intro[0], "type": "self_intro"}] +
        [{"text": t, "type": "technical"} for t in technical] +
        [{"text": aptitude[0], "type": "aptitude"}] +
        [{"text": c, "type": "coding"} for c in coding]
    )

    interviews_collection.update_one(
        {"_id": ObjectId(interview_id)},
        {"$set": {
            "ordered_questions": ordered_questions,
            "current_index": 0,
            "status": "questions_generated"
        }}
    )

    return {"total_questions": len(ordered_questions)}

# =================================================
# NEXT QUESTION
# =================================================
@router.post("/next-question")
def next_question(interview_id: str = Form(...)):
    interview = interviews_collection.find_one({"_id": ObjectId(interview_id)})
    questions = interview.get("ordered_questions")

    if not questions:
        raise HTTPException(400, "Questions not generated")

    idx = interview.get("current_index", 0)
    if idx >= len(questions):
        return {"message": "Interview completed"}

    q = questions[idx]
    return {
        "question_number": idx + 1,
        "question": q["text"],
        "question_type": q["type"]
    }

# =================================================
# SUBMIT ANSWER
# =================================================
@router.post("/submit-answer")
def submit_answer(
    interview_id: str = Form(...),
    question: str = Form(...),
    question_type: str = Form(...),
    answer: Optional[str] = Form("")
):
    interviews_collection.update_one(
        {"_id": ObjectId(interview_id)},
        {
            "$push": {
                "answers": {
                    "question": question,
                    "type": question_type,
                    "answer": answer.strip(),
                    "attempted": bool(answer.strip())
                }
            },
            "$inc": {"current_index": 1}
        }
    )
    return {"ok": True}

# =================================================
# FINAL EVALUATION (PERFECT LOGIC)
# =================================================
@router.post("/evaluate")
def evaluate_interview(interview_id: str = Form(...)):
    interview = interviews_collection.find_one({"_id": ObjectId(interview_id)})
    answers = interview.get("answers", [])

    section_scores = {k: [] for k in ["self_intro", "technical", "aptitude", "coding"]}
    section_feedback = {k: [] for k in ["self_intro", "technical", "aptitude", "coding"]}

    for a in answers:
        if not a["attempted"]:
            continue

        qtype = a["type"]

        # -------- CODING (RULE-BASED) --------
        if qtype == "coding":
            result = analyze_code(a["answer"])
        else:
            result = evaluate_answer(
                question=a["question"],
                answer=a["answer"],
                category=qtype
            )

        section_scores[qtype].append(result["score"])
        section_feedback[qtype].append({
            "question": a["question"],
            "answer": a["answer"],
            "score": result["score"],
            "strengths": result["strengths"],
            "weaknesses": result["weaknesses"],
            "suggestions": result["suggestions"]
        })

    def avg(x): return round(sum(x) / len(x), 2) if x else None

    scores = {
        "resume": interview["resume_score"],
        "self_intro": avg(section_scores["self_intro"]),
        "technical": avg(section_scores["technical"]),
        "aptitude": avg(section_scores["aptitude"]),
        "coding": avg(section_scores["coding"]),
    }

    scores["final"] = calculate_final_score(
        scores["resume"],
        scores["technical"],
        scores["aptitude"],
        scores["coding"]
    )

    decision = "Selected" if scores["final"] >= 70 else "Rejected"

    interviews_collection.update_one(
        {"_id": ObjectId(interview_id)},
        {"$set": {
            "scores": scores,
            "feedback": section_feedback,
            "decision": decision,
            "status": "completed"
        }}
    )

    return {"scores": scores, "feedback": section_feedback, "decision": decision}

# =================================================
# RESULT FETCH
# =================================================
@router.get("/result/{interview_id}")
def get_result(interview_id: str):
    interview = interviews_collection.find_one({"_id": ObjectId(interview_id)})
    if not interview or "scores" not in interview:
        raise HTTPException(404, "Result not found")

    return {
        "scores": interview["scores"],
        "feedback": interview["feedback"],
        "decision": interview["decision"]
    }
