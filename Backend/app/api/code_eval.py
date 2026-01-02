from fastapi import APIRouter, Body
from app.services.code_analyzer import analyze_code

router = APIRouter(prefix="/api/code", tags=["Code Evaluation"])


@router.post("/evaluate")
def evaluate_code(code: str = Body(..., embed=True)):
    """
    Evaluates coding answer and returns score scaled to 0–100
    """
    raw_score = analyze_code(code)  # expected 0–10 or 0–1 or heuristic

    # 🔥 Normalize to 0–100 safely
    if raw_score <= 1:
        score = round(raw_score * 100, 2)
    elif raw_score <= 10:
        score = round((raw_score / 10) * 100, 2)
    else:
        score = min(round(raw_score, 2), 100)

    return {
        "score": score,
        "max_score": 100,
        "verdict": "Good" if score >= 60 else "Needs Improvement"
    }
