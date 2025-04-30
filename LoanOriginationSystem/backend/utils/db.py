from pymongo import MongoClient
import os

# MongoDB connection string from the environment 
MONGO_URI = os.getenv('MONGO_URI')

# Make sure we have a MongoDB URI
if not MONGO_URI:
    raise ValueError("MONGO_URI environment variable is required but not set")

# Database name
DB_NAME = 'loan_origination_system'

# MongoDB client instance
_client = None

def get_client():
    """Get MongoDB client instance."""
    global _client
    if _client is None:
        # Configure connection to MongoDB Atlas
        # Note: SSL/TLS settings are included in the connection string
        _client = MongoClient(
            MONGO_URI,
            retryWrites=True,
            connectTimeoutMS=30000,
            socketTimeoutMS=30000,
            serverSelectionTimeoutMS=30000,
            tlsAllowInvalidCertificates=True  # For testing purposes only
        )
    return _client

def get_db():
    """Get MongoDB database instance."""
    client = get_client()
    return client[DB_NAME]

def close_connection():
    """Close MongoDB connection."""
    global _client
    if _client is not None:
        _client.close()
        _client = None
