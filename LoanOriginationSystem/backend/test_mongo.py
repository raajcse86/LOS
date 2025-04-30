import os
import sys
from pymongo import MongoClient
import time

# Add path for local imports
sys.path.append('.')

print("Starting MongoDB connection test...")

# MongoDB connection string from the environment
mongo_uri = os.getenv('MONGO_URI')

if not mongo_uri:
    print("ERROR: MONGO_URI environment variable is not set!")
    sys.exit(1)

print("MONGO_URI is set")

try:
    # Try to connect to MongoDB with correct connection settings
    print("Connecting to MongoDB...")
    client = MongoClient(
        mongo_uri, 
        serverSelectionTimeoutMS=5000,
        connectTimeoutMS=30000,
        socketTimeoutMS=30000,
        tlsAllowInvalidCertificates=True  # For testing purposes only
    )
    
    # Check if connection was successful
    print("Checking server info...")
    server_info = client.server_info()
    print(f"Successfully connected to MongoDB: {server_info['version']}")
    
    # Test database operations
    db = client['loan_origination_system']
    print("Checking database access...")
    
    # List collections
    collections = db.list_collection_names()
    print(f"Collections in database: {collections}")
    
    # Test document insertion
    test_collection = db['test_connection']
    result = test_collection.insert_one({"test": "data", "timestamp": time.time()})
    print(f"Test document inserted with ID: {result.inserted_id}")
    
    # Cleanup
    test_collection.delete_one({"_id": result.inserted_id})
    print("Test document deleted")
    
    print("MongoDB connection and operations test successful!")
    
except Exception as e:
    print(f"ERROR: Failed to connect to MongoDB: {e}")
    sys.exit(1)