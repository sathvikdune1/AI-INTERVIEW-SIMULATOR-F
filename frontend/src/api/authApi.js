from fastapi import APIRouter, HTTPException
from app.db.mongodb import users_collection
from app.core.security import hash_password, verify_password, create_token
from datetime import datetime
from pydantic import BaseModel

router = APIRouter(prefix="/api/auth", tags=["Auth"])


# ✅ Request Model
class UserRequest(BaseModel):
    username: str
    email: str
    password: str


@router.post("/register")
def register(user: UserRequest):

    existing = users_collection.find_one({"username": user.username})
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    user_data = user.dict()
    user_data["password"] = hash_password(user.password)
    user_data["created_at"] = datetime.utcnow()

    users_collection.insert_one(user_data)

    return {"message": "User registered successfully"}


@router.post("/login")
def login(user: UserRequest):

    db_user = users_collection.find_one({"username": user.username})

    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_token(str(db_user["_id"]))

    return {
        "token": token,
        "user": {
            "id": str(db_user["_id"]),
            "username": db_user["username"]
        }
    }
