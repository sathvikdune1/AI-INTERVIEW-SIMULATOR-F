from fastapi import APIRouter

router = APIRouter()

@router.post("/evaluate")
def evaluate():
    return {"score": 80}
