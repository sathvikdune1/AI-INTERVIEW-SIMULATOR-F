from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime

from app.db.mongodb import users_collection
from app.core.security import hash_password, verify_password, create_token

router = APIRouter(prefix="/api/auth", tags=["Auth"])


# ✅ Pydantic Models
class UserRegister(BaseModel):
    username: str
    email: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


# ✅ REGISTER API
@router.post("/register")
def register(user: UserRegister):

    existing = users_collection.find_one({"username": user.username})
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_password = hash_password(user.password)

    new_user = {
        "username": user.username,
        "email": user.email,
        "password": hashed_password,
        "created_at": datetime.utcnow()
    }

    users_collection.insert_one(new_user)

    return {"message": "User registered successfully"}


# ✅ LOGIN API
@router.post("/login")
def login(user: UserLogin):

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
            "username": db_user["username"],
            "email": db_user["email"]
        }
    }
