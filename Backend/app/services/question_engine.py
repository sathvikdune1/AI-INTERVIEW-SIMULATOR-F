"""
Question Engine Service (LOCAL LLM)
----------------------------------
- Generates interview questions dynamically
- Uses FLAN-T5 locally (no API, no internet)
"""

from transformers import pipeline


# Load model once (this may take 20–40 seconds first time)
question_generator = pipeline(
    "text2text-generation",
    model="google/flan-t5-base",
    max_length=128
)


def get_difficulty_from_resume_score(resume_score: int) -> str:
    if resume_score >= 15:
        return "hard"
    elif resume_score >= 8:
        return "medium"
    return "easy"


def generate_question(skills: list, difficulty: str) -> str:
    prompt = (
        f"Generate one {difficulty} technical interview question "
        f"based on these skills: {', '.join(skills)}"
    )

    result = question_generator(prompt)
    return result[0]["generated_text"]


# -----------------------------
# Test Runner
# -----------------------------
if __name__ == "__main__":
    skills = ["python", "machine learning", "aws"]
    resume_score = 18

    difficulty = get_difficulty_from_resume_score(resume_score)
    question = generate_question(skills, difficulty)

    print("\nDifficulty:", difficulty)
    print("Generated Question:\n", question)
