from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Header
from bson import ObjectId
from datetime import datetime, timezone
from typing import Optional
import os, shutil

from Backend.app.services.resume_parser import analyze_resume
from Backend.app.services.dynamic_question_engine import generate_interview_questions
from Backend.app.services.gemini_answer_evaluator import evaluate_answer
from Backend.app.services.scoring_engine import calculate_final_score
from Backend.app.services.code_analyzer import analyze_code
from Backend.app.services.vision_analysis import analyze_frame

from Backend.app.db.mongodb import interviews_collection
from Backend.app.core.security import decode_token

from pydantic import BaseModel
import base64
import numpy as np
import cv2


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
    difficulty: str = Form(...),
    authorization: str = Header(None)
):

    final_name = name or full_name
    if not final_name:
        raise HTTPException(400, "Name required")

    user_id = None

    if authorization:
        token = authorization.split(" ")[1]
        user_id = decode_token(token)

    interview = {
        "user_id": user_id,
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
# GET USER INTERVIEWS (HOME PAGE)
# =================================================
@router.get("/user")
def get_user_interviews(authorization: str = Header(None)):

    interviews = interviews_collection.find({
        "status": "completed"
    }).sort("created_at", -1)

    result = []

    for i in interviews:

        # Handle both formats safely
        role = i.get("job_role") or i.get("role") or "Unknown Role"

        score = 0
        if "scores" in i:
            score = i.get("scores", {}).get("final", 0)
        else:
            score = i.get("score", 0)

        result.append({
            "_id": str(i["_id"]),
            "role": role,
            "difficulty": i.get("difficulty", "medium"),
            "score": score,
            "created_at": i.get("created_at")
        })

    return result


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
# GENERATE QUESTIONS
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

    self_intro = q.get("self_intro", [])[:1] or [
        "Can you briefly introduce yourself?"
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
# FINAL EVALUATION
# =================================================
@router.post("/evaluate")
def evaluate_interview(interview_id: str = Form(...)):

    interview = interviews_collection.find_one({"_id": ObjectId(interview_id)})

    if not interview:
        raise HTTPException(404, "Interview not found")

    answers = interview.get("answers", [])

    section_scores = {
        "self_intro": [],
        "technical": [],
        "aptitude": [],
        "coding": []
    }

    section_feedback = {
        "self_intro": [],
        "technical": [],
        "aptitude": [],
        "coding": []
    }

    for a in answers:

        if not a["attempted"]:
            continue

        qtype = a["type"]

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
            "strengths": result.get("strengths", []),
            "weaknesses": result.get("weaknesses", []),
            "suggestions": result.get("suggestions", [])
        })

    def avg(arr):
        return round(sum(arr) / len(arr), 2) if arr else 0

    scores = {
        "resume": interview.get("resume_score", 0),
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
        {
            "$set": {
                "scores": scores,
                "feedback": section_feedback,
                "decision": decision,
                "status": "completed"
            }
        }
    )

    return {
        "scores": scores,
        "feedback": section_feedback,
        "decision": decision
    }


# =================================================
# RESULT FETCH
# =================================================
@router.get("/result/{interview_id}")
def get_result(interview_id: str):

    interview = interviews_collection.find_one({"_id": ObjectId(interview_id)})

    if not interview:
        raise HTTPException(404, "Result not found")

    return {
        "scores": interview.get("scores"),
        "feedback": interview.get("feedback"),
        "decision": interview.get("decision")
    }


# =================================================
# VISION ANALYSIS
# =================================================
class VisionRequest(BaseModel):
    image: str


@router.post("/analyze-vision")
def analyze_vision(data: VisionRequest):

    try:

        image_data = data.image

        if "," in image_data:
            image_data = image_data.split(",")[1]

        img_bytes = base64.b64decode(image_data)

        np_arr = np.frombuffer(img_bytes, np.uint8)

        frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        if frame is None:
            raise HTTPException(400, "Invalid image")

        result = analyze_frame(frame)

        return result

    except Exception as e:

        raise HTTPException(500, str(e))