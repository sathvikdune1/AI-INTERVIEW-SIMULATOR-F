import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")

if not MONGODB_URI:
    raise ValueError("MONGODB_URI not found in .env file")

client = MongoClient(
    MONGODB_URI,
    tls=True,
    serverSelectionTimeoutMS=5000
)

db = client["ai_interview_db"]

interviews_collection = db["interviews"]
users_collection = db["users"]
questions_collection = db["questions"]

def ping_db():
    client.admin.command("ping")