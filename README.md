# Recipe Manager

A Streamlit-based web application for managing and sharing recipes.

## Features

- Store and manage user-submitted recipes
- Categorize recipes with tags (e.g., vegan, gluten-free, spicy)
- Search recipes by name, ingredients, or tags
- Public and private recipe sharing options
- Anonymous recipe submission
- User authentication system
- Image upload support for recipes

## Installation

1. Clone this repository
2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the application:
```bash
streamlit run app.py
```

2. Open your web browser and navigate to the URL shown in the terminal (typically http://localhost:8501)

## Features

- **Home**: View featured recipes
- **Add Recipe**: Submit new recipes with details and images
- **Search Recipes**: Find recipes by name, ingredients, or tags
- **Login/Register**: Create an account or sign in to access additional features

## Data Storage

The application stores data locally in JSON files:
- `data/recipes.json`: Stores recipe information
- `data/users.json`: Stores user account information
- `data/`: Directory for storing recipe images

## Security Notes

- Passwords are stored in plain text (for demonstration purposes only)
- In a production environment, implement proper password hashing and security measures
- Consider using a proper database system for production use 