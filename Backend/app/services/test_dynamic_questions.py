from Backend.app.services.dynamic_question_engine import generate_interview_questions

# Simulated extracted resume skills
resume_skills = [
    "python",
    "machine learning",
    "docker",
    "aws",
    "sql"
]

job_role = "AI/ML Engineer"
difficulty = "intermediate"

# Generate questions
questions = generate_interview_questions(
    resume_skills=resume_skills,
    job_role=job_role,
    difficulty=difficulty
)

print("\n--- GENERATED INTERVIEW QUESTIONS ---\n")

# SELF INTRO
print("[SELF INTRODUCTION]")
for i, q in enumerate(questions["self_intro"], 1):
    print(f"{i}. {q}")
print()

# TECHNICAL
print("[TECHNICAL QUESTIONS]")
for i, q in enumerate(questions["technical"], 1):
    print(f"{i}. {q}")
print()

# APTITUDE
print("[APTITUDE QUESTIONS]")
for i, q in enumerate(questions["aptitude"], 1):
    print(f"{i}. {q}")
print()

# CODING
print("[CODING QUESTIONS]")
for i, q in enumerate(questions["coding"], 1):
    print(f"{i}. {q}")
print()
