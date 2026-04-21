from Backend.app.services.gemini_answer_evaluator import evaluate_answer
from Backend.app.services.code_quality_evaluator import evaluate_code


def evaluate_by_type(question, answer, qtype):

    if qtype == "coding":
        return evaluate_code(question, answer)

    return evaluate_answer(question, answer, qtype)