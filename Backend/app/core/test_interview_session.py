from Backend.app.core.interview_session_controller import run_interview_session

# Simulated answers
answers = {
    1: "I am an AI/ML engineer with strong Python and ML experience.",
    2: "Supervised learning uses labeled data.",
    3: "Docker helps by containerizing applications.",
    4: "Overfitting happens when a model memorizes data.",
    5: "AWS helps in scalable ML deployment.",
    6: "SQL uses structured tables, NoSQL is flexible.",
    7: "If workers double, time halves.",
    8: "def second_largest(lst): return sorted(lst)[-2]",
    9: "def is_palindrome(s): return s == s[::-1]"
}

run_interview_session(
    candidate_name="Dune Sankar Narayan Sathvik",
    email="sathvikdune1@gmail.com",
    phone="6303439522",
    job_role="AI/ML Engineer",
    difficulty="hard",
    resume_pdf_path="Backend/app/db/resumes/sample_resume.pdf",
    candidate_answers=answers
)
