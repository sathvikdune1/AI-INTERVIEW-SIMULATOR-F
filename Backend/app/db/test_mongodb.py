from datetime import datetime, timezone
from app.db.mongodb import interviews_collection, ping_db

def test_mongodb():
    print("\n--- TESTING MONGODB CONNECTION ---")

    # Ping DB
    ping_db()
    print("MongoDB connection successful")

    # Test insert
    test_doc = {
        "candidate_name": "Dune Sankar Narayan Sathvik",
        "role": "AI/ML Engineer",
        "score": 88,
        "created_at": datetime.now(timezone.utc)
    }

    result = interviews_collection.insert_one(test_doc)
    print("Inserted document ID:", result.inserted_id)

    # Fetch back
    record = interviews_collection.find_one({"_id": result.inserted_id})
    print("Fetched Record:", record)


if __name__ == "__main__":
    test_mongodb()