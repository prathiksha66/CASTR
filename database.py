from pymongo import MongoClient

# Connect to local MongoDB server
client = MongoClient("mongodb://localhost:27017/")

# CASTR database
db = client["castr_db"]

# Collections
users = db["users"]
actors = db["actors"]
productions = db["productions"]
roles = db["roles"]
applications = db["applications"]
auditions = db["auditions"]
evaluations = db["evaluations"]

# Test connection
try:
    client.admin.command("ping")
    print("MongoDB connected successfully!")
except Exception as e:
    print("MongoDB connection failed:", e)