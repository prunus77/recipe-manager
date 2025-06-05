from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
import streamlit as st
import time
from functools import wraps
import os

# MongoDB connection settings with retry logic
def get_mongo_client(max_retries=3, retry_delay=1):
    """Create MongoDB client with retry logic"""
    for attempt in range(max_retries):
        try:
            # Try to get connection string from environment variable first
            MONGO_URI = os.getenv('MONGODB_CONNECTION_STRING')
            if not MONGO_URI:
                # Fallback to Streamlit secrets
                try:
                    MONGO_URI = st.secrets["mongodb"]["connection_string"]
                except:
                    # Fallback to local connection if secrets not available
                    MONGO_URI = "mongodb://localhost:27017/"
            
            client = MongoClient(
                MONGO_URI,
                serverSelectionTimeoutMS=2000,  # Reduced timeout
                connectTimeoutMS=2000,
                maxPoolSize=10,  # Reduced pool size
                minPoolSize=5,
                maxIdleTimeMS=30000,  # Close idle connections after 30 seconds
                waitQueueTimeoutMS=2000,  # Wait queue timeout
                retryWrites=True,
                retryReads=True
            )
            # Test the connection
            client.admin.command('ping')
            return client
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            if attempt == max_retries - 1:  # Last attempt
                st.error(f"Failed to connect to MongoDB after {max_retries} attempts: {str(e)}")
                raise
            time.sleep(retry_delay)
    return None

# Lazy initialization of database connection
_db = None
_client = None

def get_db():
    """Get database instance with lazy initialization"""
    global _db, _client
    if _db is None:
        try:
            _client = get_mongo_client()
            _db = _client["recipe_manager"]
            init_db(_db)
        except Exception as e:
            st.error(f"Database initialization failed: {str(e)}")
            raise
    return _db

def init_db(db):
    """Initialize database collections and indexes"""
    try:
        # Create indexes for users collection
        db.users.create_index("username", unique=True)
        db.users.create_index("email", unique=True)
        
        # Create indexes for recipes collection
        db.recipes.create_index("name")
        db.recipes.create_index("category")
        db.recipes.create_index("tags")
        db.recipes.create_index("created_by")
    except Exception as e:
        st.error(f"Failed to create indexes: {str(e)}")
        raise

# Decorator for database operations with caching
def with_db_retry(max_retries=3, retry_delay=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except (ConnectionFailure, ServerSelectionTimeoutError) as e:
                    if attempt == max_retries - 1:
                        st.error(f"Database operation failed after {max_retries} attempts: {str(e)}")
                        raise
                    time.sleep(retry_delay)
            return None
        return wrapper
    return decorator

# Collections access functions
def get_users_collection():
    return get_db().users

def get_recipes_collection():
    return get_db().recipes 