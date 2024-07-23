from pymongo import MongoClient
import os

# MongoDB setup
client = MongoClient(os.environ["MONGODB_URI"])
db = client.your_database_name

# Test insertion
test_data = {"name": "Test User", "email": "test@example.com"}
result = db.test_collection.insert_one(test_data)
print(f"Inserted document with ID: {result.inserted_id}")

# Test retrieval
retrieved = db.test_collection.find_one({"name": "Test User"})
print(f"Retrieved document: {retrieved}")

# Clean up
db.test_collection.delete_one({"name": "Test User"})
print("Test document deleted")

print("MongoDB connection test completed successfully!")
