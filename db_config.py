from pymongo import MongoClient

# MongoDB connection settings
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "recipe_manager"

# Create MongoDB client
client = MongoClient(MONGO_URI)
db = client[DB_NAME]

# Collections
users_collection = db.users
recipes_collection = db.recipes

# Initialize collections with indexes
def init_db():
    # Create indexes for users collection
    users_collection.create_index("username", unique=True)
    users_collection.create_index("email", unique=True)
    
    # Create indexes for recipes collection
    recipes_collection.create_index("name")
    recipes_collection.create_index("category")
    recipes_collection.create_index("tags")
    recipes_collection.create_index("created_by")

# Call initialization
init_db() 