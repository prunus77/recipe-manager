from pymongo import MongoClient
from datetime import datetime
import bcrypt
import os
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
from db_config import get_users_collection, get_recipes_collection, with_db_retry
from bson import ObjectId

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
        hashed_password = bcrypt.hashpw(admin_password.encode('utf-8'), bcrypt.gensalt())
        users.insert_one({
            'username': 'admin',
            'password': hashed_password,
            'role': 'admin',
            'created_at': datetime.now(),
            'email': 'admin@recipemanager.com'
        })

@with_db_retry()
def create_user(username, password, email):
    """Create a new user with retry logic"""
    users = get_users_collection()
    
    # Check if username or email already exists
    if users.find_one({"$or": [{"username": username}, {"email": email}]}):
        return False, "Username or email already exists"
    
    # Hash password
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    # Create user document
    user = {
        "username": username,
        "password": hashed,
        "email": email,
        "role": "user",
        "created_at": datetime.utcnow(),
        "is_active": True
    }
    
    try:
        users.insert_one(user)
        return True, "User created successfully"
    except Exception as e:
        return False, f"Failed to create user: {str(e)}"

@with_db_retry()
def verify_user(username, password):
    """Verify user credentials with retry logic"""
    users = get_users_collection()
    user = users.find_one({"username": username})
    
    if not user:
        return False, "User not found"
    
    if not user.get("is_active", True):
        return False, "User account is inactive"
    
    if bcrypt.checkpw(password.encode('utf-8'), user["password"]):
        return True, {
            "username": user["username"],
            "role": user.get("role", "user")
        }
    
    return False, "Invalid password"

@with_db_retry()
def get_all_users():
    """Get all users with retry logic"""
    users = get_users_collection()
    return list(users.find({}, {"password": 0}))

@with_db_retry()
def update_user_status(username, is_active):
    """Update user status with retry logic"""
    users = get_users_collection()
    result = users.update_one(
        {"username": username},
        {"$set": {"is_active": is_active}}
    )
    return result.modified_count > 0

@with_db_retry()
def delete_user(username):
    """Delete user with retry logic"""
    users = get_users_collection()
    result = users.delete_one({"username": username})
    return result.deleted_count > 0

@with_db_retry()
def get_user_stats():
    """Get user statistics with retry logic"""
    users = get_users_collection()
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

# Recipe-related functions
@with_db_retry()
def get_all_recipes():
    """Get all recipes with retry logic"""
    recipes = get_recipes_collection()
    return list(recipes.find())

@with_db_retry()
def get_recipe_by_id(recipe_id):
    """Get recipe by ID with retry logic"""
    recipes = get_recipes_collection()
    return recipes.find_one({"_id": ObjectId(recipe_id)})

@with_db_retry()
def create_recipe(recipe_data):
    """Create new recipe with retry logic"""
    recipes = get_recipes_collection()
    recipe_data["created_at"] = datetime.utcnow()
    result = recipes.insert_one(recipe_data)
    return result.inserted_id

@with_db_retry()
def update_recipe(recipe_id, recipe_data):
    """Update recipe with retry logic"""
    recipes = get_recipes_collection()
    result = recipes.update_one(
        {"_id": ObjectId(recipe_id)},
        {"$set": recipe_data}
    )
    return result.modified_count > 0

@with_db_retry()
def delete_recipe(recipe_id):
    """Delete recipe with retry logic"""
    recipes = get_recipes_collection()
    result = recipes.delete_one({"_id": ObjectId(recipe_id)})
    return result.deleted_count > 0

# Initialize database
init_db() 