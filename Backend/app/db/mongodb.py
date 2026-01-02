import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")

if not MONGODB_URI:
    raise ValueError("MONGODB_URI not found in .env file")

# Create MongoDB client
client = MongoClient(
    MONGODB_URI,
    tls=True,
    serverSelectionTimeoutMS=5000
)

# Database
db = client["ai_interview_db"]

# Collections
interviews_collection = db["interviews"]
users_collection = db["users"]
questions_collection = db["questions"]

def ping_db():
    """Check MongoDB connection"""
    client.admin.command("ping")
