from sentence_transformers import SentenceTransformer, util
from typing import List, Optional
from datetime import datetime, timezone
from Backend.app.db.mongodb import interviews_collection  

model = SentenceTransformer("all-MiniLM-L6-v2")
MAX_CHARS = 500


def _safe(text: str) -> str:
    return text[:MAX_CHARS] if text else ""


# --------------------------------------------------
# SEMANTIC SIMILARITY
# --------------------------------------------------
def similarity_score(a: str, b: str) -> float:
    if not a or not b:
        return 0.0
    a, b = _safe(a), _safe(b)
    emb_a = model.encode(a, convert_to_tensor=True)
    emb_b = model.encode(b, convert_to_tensor=True)
    return max(util.cos_sim(emb_a, emb_b).item(), 0) * 100


# --------------------------------------------------
# SELF INTRO SCORING
# --------------------------------------------------
def score_self_intro_answers(answers: List[dict]) -> Optional[float]:
    scores = []

    for a in answers:
        ans = a.get("answer", "").strip()

        if len(ans.split()) < 20:
            scores.append(40)

        elif len(ans.split()) < 40:
            scores.append(60)

        else:
            scores.append(85)

    return sum(scores) / len(scores) if scores else 0


# --------------------------------------------------
# TECHNICAL SCORING
# --------------------------------------------------
def score_technical_answers(answers: List[dict]) -> Optional[float]:
    scores = []

    for a in answers:
        ref = f"Explain {a.get('question')}"
        scores.append(similarity_score(a.get("answer", ""), ref))

    return sum(scores) / len(scores) if scores else 0


# --------------------------------------------------
# APTITUDE SCORING
# --------------------------------------------------
def score_aptitude_answers(answers: List[dict]) -> Optional[float]:
    scores = []

    for a in answers:
        ans = a.get("answer", "")
        tokens = len(ans.split())

        if tokens >= 10:
            scores.append(80)

        elif tokens >= 5:
            scores.append(60)

        else:
            scores.append(40)

    return sum(scores) / len(scores) if scores else 0


# --------------------------------------------------
# SAVE INTERVIEW RESULT (NEW FUNCTION)
# --------------------------------------------------
def save_interview_result(
    candidate_name: str,
    role: str,
    final_score: float
):
    interview_data = {
        "candidate_name": candidate_name,
        "role": role,
        "score": final_score,
        "created_at": datetime.now(timezone.utc)
    }

    interviews_collection.insert_one(interview_data)


# --------------------------------------------------
# FINAL SCORE (WEIGHTED)
# --------------------------------------------------
def calculate_final_score(
    resume_score,
    technical_score,
    aptitude_score,
    coding_score
):

    weights = {
        "resume": 0.15,
        "technical": 0.40,
        "aptitude": 0.20,
        "coding": 0.25
    }

    scores = {
        "resume": resume_score or 0,
        "technical": technical_score or 0,
        "aptitude": aptitude_score or 0,
        "coding": coding_score or 0
    }

    final = (
        scores["resume"] * weights["resume"] +
        scores["technical"] * weights["technical"] +
        scores["aptitude"] * weights["aptitude"] +
        scores["coding"] * weights["coding"]
    )

    return round(final, 2)
    # --------------------------------------------------
    # SAVE RESULT TO MONGODB
    # --------------------------------------------------
    try:
        save_interview_result(candidate_name, role, final_score)
    except Exception as e:
        print("Failed to save interview result:", e)

    return final_score