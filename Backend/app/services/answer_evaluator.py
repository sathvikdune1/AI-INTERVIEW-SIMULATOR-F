from Backend.app.services.gemini_answer_evaluator import evaluate_answer
from Backend.app.services.code_quality_evaluator import evaluate_code


def evaluate_by_type(question, answer, qtype):
    if qtype in ["self_intro", "technical"]:
        return evaluate_answer(question, answer, qtype)

    if qtype == "aptitude":
        return evaluate_answer(
            question,
            answer,
            "aptitude (mathematical correctness)"
        )

    if qtype == "coding":
        return evaluate_code(question, answer)

    return {
        "score": 0,
        "strengths": [],
        "weaknesses": ["Unknown question type"],
        "suggestions": []
    }
