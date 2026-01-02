import ast

def evaluate_code(question, code):
    feedback = {
        "strengths": [],
        "weaknesses": [],
        "suggestions": []
    }

    score = 50

    try:
        tree = ast.parse(code)
        score += 20
        feedback["strengths"].append("Code syntax is valid")
    except Exception:
        feedback["weaknesses"].append("Syntax errors present")
        feedback["suggestions"].append("Fix syntax issues before submission")
        return {**feedback, "score": 30}

    if "def " in code:
        score += 10
        feedback["strengths"].append("Function definition used")

    if "return" in code:
        score += 10
        feedback["strengths"].append("Return statement present")

    if "if" in code:
        score += 5
        feedback["strengths"].append("Conditional logic included")
    else:
        feedback["weaknesses"].append("No edge case handling")
        feedback["suggestions"].append("Handle edge cases using conditionals")

    if "try" not in code:
        feedback["suggestions"].append("Add error handling (try/except)")

    score = min(score, 95)

    return {
        "score": score,
        **feedback
    }
