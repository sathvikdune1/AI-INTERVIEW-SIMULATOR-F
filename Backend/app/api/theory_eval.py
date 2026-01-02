from fastapi import APIRouter
from app.services.nlp_scoring import score_theory

router = APIRouter()

@router.post("/evaluate")
def evaluate(answer: str):
    return {"score": score_theory(answer)}
