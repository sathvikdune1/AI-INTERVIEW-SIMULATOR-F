from fastapi import APIRouter, Header, HTTPException
from Backend.app.db.mongodb import interviews_collection
from Backend.app.core.security import decode_token

router = APIRouter(prefix="/api/results", tags=["Results"])


@router.get("/{interview_id}")
def get_results(interview_id: str, authorization: str = Header(None)):

    if not authorization:
        raise HTTPException(status_code=401, detail="Unauthorized")

    token = authorization.split(" ")[1]

    user_id = decode_token(token)

    interview = interviews_collection.find_one({
        "_id": interview_id,
        "user_id": user_id
    })

    if not interview:
        raise HTTPException(status_code=404, detail="Not found")

    return {
        "breakdown": interview["scores"],
        "final_score": interview["scores"]["final"],
        "decision": interview["decision"],
        "created_at": interview.get("created_at")
    }