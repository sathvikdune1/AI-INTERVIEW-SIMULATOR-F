from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("all-MiniLM-L6-v2")

def score_theory(answer: str, reference: str) -> float:
    if not answer or not reference:
        return 0.0

    emb1 = model.encode(answer, convert_to_tensor=True)
    emb2 = model.encode(reference, convert_to_tensor=True)

    score = float(util.cos_sim(emb1, emb2)) * 100

    # Clamp score between 0 and 100
    return round(max(0, min(score, 100)), 2)
