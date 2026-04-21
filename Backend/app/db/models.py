from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")

db = client["ai_interview"]

interviews = db["interviews"]
users = db["users"]