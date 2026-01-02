from sentence_transformers import SentenceTransformer, util
from typing import List, Optional

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
        ans = a.get("answer","").strip()
        if len(ans.split()) < 20:
            scores.append(40)
        elif len(ans.split()) < 40:
            scores.append(60)
        else:
            scores.append(85)
    return sum(scores)/len(scores) if scores else 0

# --------------------------------------------------
# TECHNICAL SCORING
# --------------------------------------------------
def score_technical_answers(answers: List[dict]) -> Optional[float]:
    scores = []
    for a in answers:
        ref = f"Explain {a.get('question')}"
        scores.append(similarity_score(a.get("answer",""), ref))
    return sum(scores)/len(scores) if scores else 0

# --------------------------------------------------
# APTITUDE SCORING
# --------------------------------------------------
def score_aptitude_answers(answers: List[dict]) -> Optional[float]:
    scores = []
    for a in answers:
        ans = a.get("answer","")
        tokens = len(ans.split())
        if tokens >= 10:
            scores.append(80)
        elif tokens >= 5:
            scores.append(60)
        else:
            scores.append(40)
    return sum(scores)/len(scores) if scores else 0

# --------------------------------------------------
# FINAL SCORE (WEIGHTED)
# --------------------------------------------------
def calculate_final_score(
    resume_score: Optional[int],
    technical_score: Optional[float],
    aptitude_score: Optional[float],
    coding_score: Optional[float]
) -> float:
    weights = {
        "resume": 0.2,
        "technical": 0.4,
        "aptitude": 0.15,
        "coding": 0.25
    }

    total, weight = 0, 0
    for s, w in [
        (resume_score, weights["resume"]),
        (technical_score, weights["technical"]),
        (aptitude_score, weights["aptitude"]),
        (coding_score, weights["coding"])
    ]:
        if s is not None:
            total += s * w
            weight += w

    return round(total / weight, 2) if weight else 0
