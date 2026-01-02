def analyze_code(code: str):
    if not code.strip():
        return {
            "score": 0,
            "strengths": [],
            "weaknesses": ["No code submitted"],
            "suggestions": ["Write a complete solution"]
        }

    score = 40
    strengths = []
    weaknesses = []
    suggestions = []

    if "def " in code:
        score += 20
        strengths.append("Function is defined")

    if "return" in code:
        score += 20
        strengths.append("Return statement used")

    if any(k in code for k in ["if", "for", "while"]):
        score += 10
        strengths.append("Logical control flow used")
    else:
        weaknesses.append("Missing control flow logic")
        suggestions.append("Use conditions or loops where required")

    if len(code.splitlines()) < 5:
        weaknesses.append("Solution is too short")
        suggestions.append("Add complete logic and edge case handling")

    score = min(score, 95)

    if not weaknesses:
        suggestions.append("Add input validation and edge case handling")

    return {
        "score": score,
        "strengths": strengths or ["Code submitted"],
        "weaknesses": weaknesses or ["Minor improvements needed"],
        "suggestions": suggestions
    }
