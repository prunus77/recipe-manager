from datetime import datetime
import os
from dotenv import load_dotenv
try:
    from werkzeug.security import generate_password_hash, check_password_hash
except ImportError:
    print("Installing werkzeug...")
    import subprocess
    subprocess.check_call(["pip", "install", "werkzeug==2.3.7"])
    from werkzeug.security import generate_password_hash, check_password_hash

from firebase_config import users_ref, recipes_ref

# Load environment variables
load_dotenv()

def init_db():
    """Initialize database with admin user if not exists"""
    admin_user = users_ref.where('role', '==', 'admin').limit(1).get()
    if not admin_user:
        admin_password = os.getenv('ADMIN_PASSWORD', 'admin123')
        hashed_password = generate_password_hash(admin_password)
        users_ref.add({
            'username': 'admin',
            'password': hashed_password,
            'role': 'admin',
            'created_at': datetime.now(),
            'email': 'admin@recipemanager.com'
        })

def create_user(username, password, email):
    try:
        # Check if username or email already exists
        existing_user = users_ref.where('username', '==', username).limit(1).get()
        existing_email = users_ref.where('email', '==', email).limit(1).get()
        
        if existing_user or existing_email:
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
        
        users_ref.add(user)
        return True, "User created successfully"
    except Exception as e:
        return False, str(e)

def verify_user(username, password):
    try:
        user_docs = users_ref.where('username', '==', username).limit(1).get()
        user = next(user_docs, None)
        
        if user and check_password_hash(user.to_dict()["password"], password):
            return True, {
                "username": user.to_dict()["username"],
                "role": user.to_dict()["role"]
            }
        return False, "Invalid username or password"
    except Exception as e:
        return False, str(e)

def get_all_users():
    try:
        users = users_ref.stream()
        return [{"id": user.id, **user.to_dict()} for user in users]
    except Exception as e:
        return []

def update_user_status(username, is_active):
    try:
        user_docs = users_ref.where('username', '==', username).limit(1).get()
        user = next(user_docs, None)
        if user:
            user.reference.update({"is_active": is_active})
            return True
        return False
    except Exception:
        return False

def delete_user(username):
    try:
        user_docs = users_ref.where('username', '==', username).limit(1).get()
        user = next(user_docs, None)
        if user:
            user.reference.delete()
            return True
        return False
    except Exception:
        return False

def get_user_stats():
    try:
        users = users_ref.stream()
        users_list = [user.to_dict() for user in users]
        
        return {
            "total_users": len(users_list),
            "active_users": sum(1 for user in users_list if user.get("is_active", True)),
            "admin_users": sum(1 for user in users_list if user.get("role") == "admin"),
            "regular_users": sum(1 for user in users_list if user.get("role") == "user")
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