"""
Interview Session Controller
----------------------------
Controls full AI interview lifecycle.
"""

from datetime import datetime, timezone
from Backend.app.services.resume_parser import (
    extract_text_from_pdf,
    extract_skills,
    calculate_resume_score
)
from Backend.app.services.dynamic_question_engine import generate_interview_questions
from Backend.app.services.nlp_scoring import score_theory
from Backend.app.services.feedback_generator import generate_feedback
from Backend.app.db.mongodb import interviews_collection


def run_interview_session(
    candidate_name: str,
    email: str,
    phone: str,
    job_role: str,
    difficulty: str,
    resume_pdf_path: str,
    candidate_answers: dict
):
    """
    candidate_answers format:
    {
        1: "answer text",
        2: "answer text",
        ...
    }
    """

    print("\n--- INTERVIEW SESSION STARTED ---")

    # -----------------------------
    # 1. Resume Parsing
    # -----------------------------
    resume_text = extract_text_from_pdf(resume_pdf_path)
    skills = extract_skills(resume_text)
    resume_score = calculate_resume_score(skills)

    print(f"Resume Score: {resume_score}")
    print(f"Extracted Skills: {skills}")

    # -----------------------------
    # 2. Generate Questions
    # -----------------------------
    questions = generate_interview_questions(
        resume_skills=skills,
        job_role=job_role,
        difficulty=difficulty
    )

    all_questions = (
        questions["self_intro"]
        + questions["technical"]
        + questions["aptitude"]
        + questions["coding"]
    )

    # -----------------------------
    # 3. Evaluate Answers
    # -----------------------------
    total_score = resume_score
    detailed_answers = []

    for idx, question in enumerate(all_questions, start=1):
        answer = candidate_answers.get(idx, "")

        nlp_score = score_theory(answer, question)
        feedback = generate_feedback(question, answer)

        total_score += nlp_score * 0.5  # weighted

        detailed_answers.append({
            "question_no": idx,
            "question": question,
            "answer": answer,
            "nlp_score": round(nlp_score, 2),
            "feedback": feedback
        })

    final_score = round(min(total_score, 100), 2)

    decision = "Selected" if final_score >= 70 else "Not Selected"

    # -----------------------------
    # 4. Store in MongoDB
    # -----------------------------
    interview_record = {
        "candidate_name": candidate_name,
        "email": email,
        "phone": phone,
        "job_role": job_role,
        "difficulty": difficulty,
        "skills": skills,
        "resume_score": resume_score,
        "final_score": final_score,
        "decision": decision,
        "responses": detailed_answers,
        "created_at": datetime.now(timezone.utc)
    }

    interviews_collection.insert_one(interview_record)

    print("\n--- INTERVIEW COMPLETED ---")
    print(f"Final Score : {final_score}")
    print(f"Decision    : {decision}")

    return interview_record
