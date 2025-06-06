from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
from db_config import users_collection, recipes_collection

# Load environment variables
load_dotenv()

# MongoDB connection
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017')
client = MongoClient(MONGO_URI)
db = client['recipe_manager']

# Collections
users = db['users']
recipes = db['recipes']

def init_db():
    """Initialize database with admin user if not exists"""
    if not users.find_one({'role': 'admin'}):
        admin_password = os.getenv('ADMIN_PASSWORD', 'admin123')
        hashed_password = generate_password_hash(admin_password)
        users.insert_one({
            'username': 'admin',
            'password': hashed_password,
            'role': 'admin',
            'created_at': datetime.now(),
            'email': 'admin@recipemanager.com'
        })

def create_user(username, password, email):
    try:
        # Check if username or email already exists
        if users.find_one({"$or": [{"username": username}, {"email": email}]}):
            return False, "Username or email already exists"
        
        # Create new user
        user = {
            "username": username,
            "password": generate_password_hash(password),
            "email": email,
            "role": "user",
            "is_active": True,
            "created_at": datetime.now()
        }
        
        users.insert_one(user)
        return True, "User created successfully"
    except Exception as e:
        return False, str(e)

def verify_user(username, password):
    try:
        user = users.find_one({"username": username})
        if user and check_password_hash(user["password"], password):
            return True, {
                "username": user["username"],
                "role": user["role"]
            }
        return False, "Invalid username or password"
    except Exception as e:
        return False, str(e)

def get_all_users():
    try:
        return list(users.find({}, {"password": 0}))
    except Exception as e:
        return []

def update_user_status(username, is_active):
    try:
        result = users.update_one(
            {"username": username},
            {"$set": {"is_active": is_active}}
        )
        return result.modified_count > 0
    except Exception:
        return False

def delete_user(username):
    try:
        result = users.delete_one({"username": username})
        return result.deleted_count > 0
    except Exception:
        return False

def get_user_stats():
    try:
        total_users = users.count_documents({})
        active_users = users.count_documents({"is_active": True})
        admin_users = users.count_documents({"role": "admin"})
        regular_users = users.count_documents({"role": "user"})
        
        return {
            "total_users": total_users,
            "active_users": active_users,
            "admin_users": admin_users,
            "regular_users": regular_users
        }
    except Exception:
        return {
            "total_users": 0,
            "active_users": 0,
            "admin_users": 0,
            "regular_users": 0
        }

# Initialize database
init_db() 