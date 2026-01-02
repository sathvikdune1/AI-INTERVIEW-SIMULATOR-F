from fastapi import APIRouter
from datetime import datetime
from Backend.app.db.mongodb import interviews_collection

router = APIRouter(prefix="/api/results", tags=["Results"])

@router.get("/{interview_id}")
def get_results(interview_id: str):
    interview = interviews_collection.find_one({"_id": interview_id})
    if not interview:
        return {"error": "Not found"}

    return {
        "breakdown": interview["scores"],
        "final_score": interview["scores"]["final"],
        "decision": interview["decision"],
        "created_at": interview.get("created_at")
    }
