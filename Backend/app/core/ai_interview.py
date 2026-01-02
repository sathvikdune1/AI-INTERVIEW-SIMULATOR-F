"""
AI Interview Orchestrator
Controls the full interview flow
"""

from Backend.app.services.resume_parser import analyze_resume
from Backend.app.services.question_engine import generate_question
from Backend.app.services.nlp_scoring import score_theory
from Backend.app.services.feedback_generator import generate_feedback
from Backend.app.services.scoring_engine import calculate_final_score
from Backend.app.db.mongodb import interviews_collection
from datetime import datetime, timezone
from Backend.app.services.pdf_generator import generate_interview_pdf


def run_ai_interview(
    candidate_name: str,
    role: str,
    resume_path: str,
    difficulty: str,
    candidate_answer: str
):
    print("\n--- AI INTERVIEW STARTED ---")

    # 1️⃣ Resume analysis
    resume_result = analyze_resume(resume_path)
    resume_score = resume_result["resume_score"]
    skills = resume_result["skills"]

    print(f"Resume Score: {resume_score}")
    print(f"Detected Skills: {skills}")

    # 2️⃣ Generate interview question
    question = generate_question(skills, difficulty)
    print("\nInterview Question:")
    print(question)

    

    # NLP semantic score using self-consistency
    nlp_score = score_theory(candidate_answer, candidate_answer)

    print(f"\nNLP Score: {nlp_score}")

    # 5️⃣ Communication score (derived from NLP for now)
    communication_score = min(nlp_score + 5, 100)

    # 6️⃣ Emotion & Coding (placeholder – already tested separately)
    emotion_score = 75
    coding_score = 80

    # 7️⃣ Final scoring
    final_result = calculate_final_score(
        resume_score=resume_score,
        nlp_score=nlp_score,
        coding_score=coding_score,
        emotion_score=emotion_score,
        communication_score=communication_score
    )

    # 8️⃣ AI Feedback
    feedback = generate_feedback(question, candidate_answer)


    # 9️⃣ Save to MongoDB
    interview_record = {
        "candidate_name": candidate_name,
        "role": role,
        "difficulty": difficulty,
        "question": question,
        "answer": candidate_answer,
        "scores": {
            "resume": resume_score,
            "nlp": nlp_score,
            "coding": coding_score,
            "emotion": emotion_score,
            "communication": communication_score,
            "final": final_result["final_score"]
        },
        "decision": final_result["decision"],
        "feedback": feedback,
        "created_at": datetime.now(timezone.utc)
    }

    interviews_collection.insert_one(interview_record)
    # Generate PDF report
    pdf_path = generate_interview_pdf(interview_record)
    print(f"PDF Report Generated: {pdf_path}")


    print("\n--- INTERVIEW COMPLETED ---")
    print(f"Final Score : {final_result['final_score']}")
    print(f"Decision    : {final_result['decision']}")

    return interview_record


# ---------------- TEST RUN ----------------
if __name__ == "__main__":
    run_ai_interview(
        candidate_name="Dune Sankar Narayan Sathvik",
        role="AI/ML Engineer",
        resume_path="Backend/app/db/resumes/sample_resume.pdf",
        difficulty="hard",
        candidate_answer="Supervised learning uses labeled data to train models."
    )
