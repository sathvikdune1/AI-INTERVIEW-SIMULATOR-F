from Backend.app.services.gemini_answer_evaluator import evaluate_answer


def score_section(section: str, answers: list):

    if not answers:
        return 0, []

    scores = []
    feedback = []

    for ans in answers:

        result = evaluate_answer(
            question=ans["question"],
            answer=ans["answer"],
            category=section
        )

        scores.append(result["score"])

        feedback.append({
            "question": ans["question"],
            "answer": ans["answer"],
            "score": result["score"],
            "strengths": result["strengths"],
            "weaknesses": result["weaknesses"],
            "suggestions": result["suggestions"]
        })

    section_score = round(sum(scores) / len(scores), 2)

    return section_score, feedback