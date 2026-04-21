from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta

SECRET_KEY = "super_secret_key"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    password = password[:72]
    return pwd_context.hash(password)


def verify_password(password: str, hashed: str):
    password = password[:72]
    return pwd_context.verify(password, hashed)


def create_token(user_id: str):

    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(hours=12)
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return token


def decode_token(token: str):

    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    return payload["user_id"]