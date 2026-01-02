def generate_feedback(question: str, answer: str) -> str:
    if not answer or len(answer.split()) < 10:
        return "Answer is too short. Add explanation and examples."

    return (
        "Strengths:\n- Relevant answer\n\n"
        "Weaknesses:\n- Could be more detailed\n\n"
        "Suggestions:\n- Use examples or edge cases"
    )
