import streamlit as st
import pandas as pd
from PIL import Image
import io
import json
from datetime import datetime
import os
from pathlib import Path
import requests
from io import BytesIO
from db_utils import (
    create_user, verify_user, get_all_users,
    update_user_status, delete_user, get_user_stats
)

# Initialize session state
if 'user' not in st.session_state:
    st.session_state.user = None
if 'user_role' not in st.session_state:
    st.session_state.user_role = None

# Create data directory if it doesn't exist
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

# File paths
RECIPES_FILE = DATA_DIR / "recipes.json"
USERS_FILE = DATA_DIR / "users.json"

def download_image(url, filename):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            image_path = DATA_DIR / filename
            with open(image_path, 'wb') as f:
                f.write(response.content)
            return str(image_path)
    except:
        return None

def init_sample_recipes():
    sample_recipes = [
        {
            'id': 1,
            'name': 'Classic Margherita Pizza',
            'category': 'Dinner',
            'tags': ['Quick', 'Vegetarian'],
            'ingredients': [
                '2 cups all-purpose flour',
                '1 cup warm water',
                '2 1/4 tsp active dry yeast',
                '1 tsp sugar',
                '1 tsp salt',
                '2 tbsp olive oil',
                '1 cup tomato sauce',
                '2 cups fresh mozzarella',
                'Fresh basil leaves',
                'Salt and pepper to taste'
            ],
            'instructions': '''1. Mix flour, yeast, sugar, and salt
2. Add warm water and olive oil, knead for 10 minutes
3. Let dough rise for 1 hour
4. Roll out dough and add toppings
5. Bake at 450°F for 15-20 minutes''',
            'is_public': True,
            'created_by': 'system',
            'created_at': datetime.now().isoformat(),
            'image_url': 'https://images.unsplash.com/photo-1604382354936-07c5d9983bd3'
        },
        {
            'id': 2,
            'name': 'Chocolate Chip Cookies',
            'category': 'Dessert',
            'tags': ['Quick', 'Budget-friendly'],
            'ingredients': [
                '2 1/4 cups flour',
                '1 cup butter, softened',
                '3/4 cup sugar',
                '3/4 cup brown sugar',
                '2 eggs',
                '1 tsp vanilla',
                '1 tsp baking soda',
                '2 cups chocolate chips'
            ],
            'instructions': '''1. Preheat oven to 375°F
2. Cream butter and sugars
3. Add eggs and vanilla
4. Mix in dry ingredients
5. Fold in chocolate chips
6. Bake for 10-12 minutes''',
            'is_public': True,
            'created_by': 'system',
            'created_at': datetime.now().isoformat(),
            'image_url': 'https://images.unsplash.com/photo-1499636136210-6f4ee915583e'
        },
        {
            'id': 3,
            'name': 'Vegetable Stir Fry',
            'category': 'Lunch',
            'tags': ['Quick', 'Vegetarian', 'Budget-friendly'],
            'ingredients': [
                '2 cups mixed vegetables',
                '2 tbsp soy sauce',
                '1 tbsp ginger, minced',
                '2 cloves garlic, minced',
                '2 tbsp vegetable oil',
                '1 tbsp cornstarch',
                '1/4 cup water'
            ],
            'instructions': '''1. Heat oil in a wok or large pan
2. Add garlic and ginger, stir for 30 seconds
3. Add vegetables and stir-fry for 5-7 minutes
4. Mix soy sauce, cornstarch, and water
5. Pour sauce over vegetables and cook until thickened''',
            'is_public': True,
            'created_by': 'system',
            'created_at': datetime.now().isoformat(),
            'image_url': 'https://images.unsplash.com/photo-1512621776951-a57141f2eefd'
        },
        {
            'id': 4,
            'name': 'Homemade Pasta Carbonara',
            'category': 'Dinner',
            'tags': ['Quick', 'Spicy'],
            'ingredients': [
                '400g spaghetti',
                '200g pancetta or bacon',
                '4 large eggs',
                '100g Pecorino Romano cheese',
                '100g Parmigiano-Reggiano',
                'Black pepper',
                'Salt'
            ],
            'instructions': '''1. Cook pasta in salted water
2. Fry pancetta until crispy
3. Mix eggs, cheese, and pepper
4. Combine hot pasta with egg mixture
5. Add pancetta and serve immediately''',
            'is_public': True,
            'created_by': 'system',
            'created_at': datetime.now().isoformat(),
            'image_url': 'https://images.unsplash.com/photo-1612874742237-6526221588e3'
        },
        {
            'id': 5,
            'name': 'Avocado Toast',
            'category': 'Breakfast',
            'tags': ['Quick', 'Vegetarian', 'Budget-friendly'],
            'ingredients': [
                '2 slices sourdough bread',
                '1 ripe avocado',
                '2 eggs',
                'Red pepper flakes',
                'Salt and pepper',
                'Lemon juice'
            ],
            'instructions': '''1. Toast the bread
2. Mash avocado with lemon juice
3. Fry eggs to desired doneness
4. Spread avocado on toast
5. Top with eggs and seasonings''',
            'is_public': True,
            'created_by': 'system',
            'created_at': datetime.now().isoformat(),
            'image_url': 'https://images.unsplash.com/photo-1588137378633-dea1336ce1e2'
        },
        {
            'id': 6,
            'name': 'Greek Salad',
            'category': 'Lunch',
            'tags': ['Vegetarian', 'Healthy', 'Quick'],
            'ingredients': [
                '2 large tomatoes',
                '1 cucumber',
                '1 red onion',
                '200g feta cheese',
                'Kalamata olives',
                'Extra virgin olive oil',
                'Red wine vinegar',
                'Dried oregano',
                'Salt and pepper'
            ],
            'instructions': '''1. Chop tomatoes and cucumber into chunks
2. Slice red onion thinly
3. Combine vegetables in a bowl
4. Add olives and crumbled feta
5. Dress with olive oil, vinegar, and seasonings''',
            'is_public': True,
            'created_by': 'system',
            'created_at': datetime.now().isoformat(),
            'image_url': 'https://images.unsplash.com/photo-1546069901-ba9599a7e63c'
        },
        {
            'id': 7,
            'name': 'Chicken Curry',
            'category': 'Dinner',
            'tags': ['Spicy', 'Comfort Food'],
            'ingredients': [
                '500g chicken thighs',
                '2 onions, diced',
                '3 cloves garlic',
                '1 tbsp ginger',
                '2 tbsp curry powder',
                '400ml coconut milk',
                '2 tbsp vegetable oil',
                'Salt to taste'
            ],
            'instructions': '''1. Heat oil and fry onions until soft
2. Add garlic, ginger, and curry powder
3. Add chicken and cook until browned
4. Pour in coconut milk and simmer
5. Cook until chicken is tender''',
            'is_public': True,
            'created_by': 'system',
            'created_at': datetime.now().isoformat(),
            'image_url': 'https://images.unsplash.com/photo-1585937421612-70a008356fbe'
        },
        {
            'id': 8,
            'name': 'Smoothie Bowl',
            'category': 'Breakfast',
            'tags': ['Vegetarian', 'Healthy', 'Quick'],
            'ingredients': [
                '2 frozen bananas',
                '1 cup frozen berries',
                '1/2 cup almond milk',
                'Toppings: granola, fresh fruit, nuts',
                'Honey or maple syrup'
            ],
            'instructions': '''1. Blend frozen bananas and berries
2. Add almond milk gradually
3. Pour into a bowl
4. Top with granola, fresh fruit, and nuts
5. Drizzle with honey or maple syrup''',
            'is_public': True,
            'created_by': 'system',
            'created_at': datetime.now().isoformat(),
            'image_url': 'https://images.unsplash.com/photo-1626074353765-517a681e40be'
        },
        {
            'id': 9,
            'name': 'Beef Tacos',
            'category': 'Dinner',
            'tags': ['Quick', 'Spicy', 'Budget-friendly'],
            'ingredients': [
                '500g ground beef',
                '1 packet taco seasoning',
                'Taco shells',
                'Lettuce, shredded',
                'Tomatoes, diced',
                'Cheese, shredded',
                'Sour cream',
                'Salsa'
            ],
            'instructions': '''1. Brown ground beef in a pan
2. Add taco seasoning and water
3. Simmer until thickened
4. Warm taco shells
5. Fill shells with beef and toppings''',
            'is_public': True,
            'created_by': 'system',
            'created_at': datetime.now().isoformat(),
            'image_url': 'https://images.unsplash.com/photo-1565299585323-38d6b0865b47'
        }
    ]
    
    # Download and save images
    for recipe in sample_recipes:
        if 'image_url' in recipe:
            image_path = download_image(recipe['image_url'], f"recipe_{recipe['id']}.jpg")
            if image_path:
                recipe['image_path'] = image_path
            del recipe['image_url']
    
    return sample_recipes

# Initialize data files if they don't exist
def init_data_files():
    if not RECIPES_FILE.exists():
        with open(RECIPES_FILE, 'w') as f:
            json.dump(init_sample_recipes(), f)
    if not USERS_FILE.exists():
        with open(USERS_FILE, 'w') as f:
            json.dump([], f)

init_data_files()

def load_data():
    with open(RECIPES_FILE, 'r') as f:
        recipes = json.load(f)
    with open(USERS_FILE, 'r') as f:
        users = json.load(f)
    return recipes, users

def save_data(recipes, users):
    with open(RECIPES_FILE, 'w') as f:
        json.dump(recipes, f)
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f)

def main():
    st.set_page_config(
        page_title="Recipe Manager",
        page_icon="🍳",
        layout="wide"
    )

    st.title("🍳 Recipe Manager")
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    
    # Initialize active_tab in session state if it doesn't exist
    if 'active_tab' not in st.session_state:
        st.session_state.active_tab = "Home"
    
    # Menu buttons in sidebar
    if st.sidebar.button("🏠 Home", use_container_width=True):
        st.session_state.active_tab = "Home"
    if st.sidebar.button("➕ Add Recipe", use_container_width=True):
        st.session_state.active_tab = "Add Recipe"
    if st.sidebar.button("📚 My Recipes", use_container_width=True):
        st.session_state.active_tab = "My Recipes"
    if st.sidebar.button("🔍 Search Recipes", use_container_width=True):
        st.session_state.active_tab = "Search Recipes"
    if st.sidebar.button("👤 Login/Register", use_container_width=True):
        st.session_state.active_tab = "Login/Register"
    
    # Add admin panel button if user is admin
    if st.session_state.user_role == 'admin':
        if st.sidebar.button("⚙️ Admin Panel", use_container_width=True):
            st.session_state.active_tab = "Admin Panel"
    
    # Add some spacing
    st.sidebar.markdown("---")
    
    # Show user status in sidebar
    if st.session_state.user:
        st.sidebar.success(f"Logged in as: {st.session_state.user}")
        if st.session_state.user_role == 'admin':
            st.sidebar.info("Role: Administrator")
        if st.button("Logout", use_container_width=True):
            st.session_state.user = None
            st.session_state.user_role = None
            st.session_state.active_tab = "Home"
            st.experimental_rerun()
    else:
        st.sidebar.info("Not logged in")

    recipes, users = load_data()

    if st.session_state.active_tab == "Home":
        st.header("Welcome to Recipe Manager!")
        st.write("Discover, share, and manage your favorite recipes.")
        
        # Display featured recipes
        st.subheader("Featured Recipes")
        if recipes:
            # Create three columns for the featured recipes
            cols = st.columns(3)
            for idx, recipe in enumerate(recipes[:9]):  # Changed from 3 to 9 recipes
                with cols[idx % 3]:  # Use modulo to cycle through columns
                    st.subheader(recipe['name'])
                    if 'image_path' in recipe and os.path.exists(recipe['image_path']):
                        st.image(recipe['image_path'], width=300)
                    st.write(f"**Category:** {recipe['category']}")
                    st.write(f"**Tags:** {', '.join(recipe['tags'])}")
                    with st.expander("View Recipe Details"):
                        st.write("**Ingredients:**")
                        for ingredient in recipe['ingredients']:
                            st.write(f"- {ingredient}")
                        st.write("**Instructions:**")
                        st.write(recipe['instructions'])

    elif st.session_state.active_tab == "My Recipes":
        st.header("My Recipes")
        
        if st.session_state.user:
            user_recipes = [r for r in recipes if r['created_by'] == st.session_state.user]
            
            if user_recipes:
                # Create a grid layout for recipes
                cols = st.columns(3)
                for idx, recipe in enumerate(user_recipes):
                    col_idx = idx % 3
                    with cols[col_idx]:
                        st.subheader(recipe['name'])
                        if 'image_path' in recipe and os.path.exists(recipe['image_path']):
                            st.image(recipe['image_path'], width=400)
                        st.write(f"**Category:** {recipe['category']}")
                        st.write(f"**Tags:** {', '.join(recipe['tags'])}")
                        st.write(f"**Created:** {datetime.fromisoformat(recipe['created_at']).strftime('%Y-%m-%d')}")
                        
                        with st.expander("View Recipe Details"):
                            st.write("**Ingredients:**")
                            for ingredient in recipe['ingredients']:
                                st.write(f"- {ingredient}")
                            st.write("**Instructions:**")
                            st.write(recipe['instructions'])
                            
                            # Add edit and delete buttons
                            col1, col2 = st.columns(2)
                            with col1:
                                if st.button("Edit Recipe", key=f"edit_{recipe['id']}"):
                                    st.session_state.editing_recipe = recipe
                                    st.experimental_rerun()
                            with col2:
                                if st.button("Delete Recipe", key=f"delete_{recipe['id']}"):
                                    recipes.remove(recipe)
                                    save_data(recipes, users)
                                    st.success("Recipe deleted successfully!")
                                    st.experimental_rerun()
            else:
                st.info("You haven't created any recipes yet. Start by adding your first recipe!")
                if st.button("Add New Recipe"):
                    st.session_state.active_tab = "Add Recipe"
                    st.experimental_rerun()
        else:
            st.warning("Please log in to view your recipes.")
            if st.button("Login"):
                st.session_state.active_tab = "Login/Register"
                st.experimental_rerun()

    elif st.session_state.active_tab == "Add Recipe":
        st.header("Add New Recipe")
        
        with st.form("recipe_form"):
            name = st.text_input("Recipe Name")
            category = st.selectbox("Category", ["Breakfast", "Lunch", "Dinner", "Dessert", "Snack"])
            tags = st.multiselect("Tags", ["Quick", "Spicy", "Budget-friendly", "Vegetarian", "Vegan", "Gluten-free"])
            
            ingredients = st.text_area("Ingredients (one per line)")
            instructions = st.text_area("Instructions")
            
            image = st.file_uploader("Recipe Image", type=['jpg', 'jpeg', 'png'])
            
            is_public = st.checkbox("Make this recipe public")
            
            submitted = st.form_submit_button("Add Recipe")
            
            if submitted:
                if name and ingredients and instructions:
                    new_recipe = {
                        'id': len(recipes) + 1,
                        'name': name,
                        'category': category,
                        'tags': tags,
                        'ingredients': [i.strip() for i in ingredients.split('\n') if i.strip()],
                        'instructions': instructions,
                        'is_public': is_public,
                        'created_by': st.session_state.user if st.session_state.user else 'anonymous',
                        'created_at': datetime.now().isoformat()
                    }
                    
                    if image:
                        # Save image to data directory
                        image_path = DATA_DIR / f"recipe_{new_recipe['id']}.{image.name.split('.')[-1]}"
                        with open(image_path, 'wb') as f:
                            f.write(image.getvalue())
                        new_recipe['image_path'] = str(image_path)
                    
                    recipes.append(new_recipe)
                    save_data(recipes, users)
                    st.success("Recipe added successfully!")
                else:
                    st.error("Please fill in all required fields.")

    elif st.session_state.active_tab == "Search Recipes":
        st.header("Search Recipes")
        
        search_term = st.text_input("Search by name or ingredients")
        selected_tags = st.multiselect("Filter by tags", ["Quick", "Spicy", "Budget-friendly", "Vegetarian", "Vegan", "Gluten-free"])
        
        filtered_recipes = recipes
        
        if search_term:
            filtered_recipes = [r for r in filtered_recipes if 
                              search_term.lower() in r['name'].lower() or
                              any(search_term.lower() in i.lower() for i in r['ingredients'])]
        
        if selected_tags:
            filtered_recipes = [r for r in filtered_recipes if 
                              any(tag in r['tags'] for tag in selected_tags)]
        
        if filtered_recipes:
            for recipe in filtered_recipes:
                with st.expander(recipe['name']):
                    if 'image_path' in recipe and os.path.exists(recipe['image_path']):
                        st.image(recipe['image_path'], width=300)
                    st.write(f"**Category:** {recipe['category']}")
                    st.write(f"**Tags:** {', '.join(recipe['tags'])}")
                    st.write("**Ingredients:**")
                    for ingredient in recipe['ingredients']:
                        st.write(f"- {ingredient}")
                    st.write("**Instructions:**")
                    st.write(recipe['instructions'])
        else:
            st.write("No recipes found matching your criteria.")

    elif st.session_state.active_tab == "Login/Register":
        st.header("Login or Register")
        
        tab1, tab2 = st.tabs(["Login", "Register"])
        
        with tab1:
            with st.form("login_form"):
                st.subheader("Login")
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                submit = st.form_submit_button("Login")
                
                if submit:
                    success, result = verify_user(username, password)
                    if success:
                        st.session_state.user = result['username']
                        st.session_state.user_role = result['role']
                        st.success("Logged in successfully!")
                        st.experimental_rerun()
                    else:
                        st.error(result)
        
        with tab2:
            with st.form("register_form"):
                new_username = st.text_input("Choose Username")
                new_password = st.text_input("Choose Password", type="password")
                confirm_password = st.text_input("Confirm Password", type="password")
                email = st.text_input("Email Address")
                register_submitted = st.form_submit_button("Register")
                
                if register_submitted:
                    if new_password != confirm_password:
                        st.error("Passwords do not match!")
                    else:
                        success, message = create_user(new_username, new_password, email)
                        if success:
                            st.success(message)
                        else:
                            st.error(message)

    elif st.session_state.active_tab == "Admin Panel":
        if st.session_state.user_role != 'admin':
            st.error("Access denied. Admin privileges required.")
            return
        
        st.header("Admin Panel")
        
        # User Statistics
        st.subheader("User Statistics")
        stats = get_user_stats()
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Users", stats['total_users'])
        with col2:
            st.metric("Active Users", stats['active_users'])
        with col3:
            st.metric("Admin Users", stats['admin_users'])
        with col4:
            st.metric("Regular Users", stats['regular_users'])
        
        # User Management
        st.subheader("User Management")
        users = get_all_users()
        
        for user in users:
            with st.expander(f"{user['username']} ({user['role']})"):
                st.write(f"Email: {user['email']}")
                st.write(f"Created: {user['created_at'].strftime('%Y-%m-%d %H:%M:%S')}")
                st.write(f"Status: {'Active' if user.get('is_active', True) else 'Inactive'}")
                
                col1, col2 = st.columns(2)
                with col1:
                    if user['username'] != 'admin':  # Prevent deactivating main admin
                        if user.get('is_active', True):
                            if st.button("Deactivate User", key=f"deactivate_{user['username']}"):
                                update_user_status(user['username'], False)
                                st.success(f"User {user['username']} deactivated")
                                st.experimental_rerun()
                        else:
                            if st.button("Activate User", key=f"activate_{user['username']}"):
                                update_user_status(user['username'], True)
                                st.success(f"User {user['username']} activated")
                                st.experimental_rerun()
                
                with col2:
                    if user['username'] != 'admin':  # Prevent deleting main admin
                        if st.button("Delete User", key=f"delete_{user['username']}"):
                            if delete_user(user['username']):
                                st.success(f"User {user['username']} deleted")
                                st.experimental_rerun()
                            else:
                                st.error("Failed to delete user")

if __name__ == "__main__":
    main() 