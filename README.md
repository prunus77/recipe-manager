# Recipe Manager

A Streamlit-based recipe management application with MongoDB integration.

## Features

- User authentication and authorization
- Recipe management (create, read, update, delete)
- Recipe categorization and tagging
- Image upload support
- Admin panel for user management
- Responsive design

## Local Development

1. Clone the repository:
```bash
git clone https://github.com/prunus77/recipe-manager.git
cd recipe-manager
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up MongoDB:
   - Install MongoDB locally or use MongoDB Atlas
   - Create a `.streamlit/secrets.toml` file with your MongoDB connection string:
```toml
[mongodb]
connection_string = "your_mongodb_connection_string"
```

5. Run the application:
```bash
streamlit run app.py
```

## Deployment on Streamlit Cloud

1. Fork this repository to your GitHub account

2. Go to [share.streamlit.io](https://share.streamlit.io/)

3. Sign in with your GitHub account

4. Click "New app"

5. Select your repository and branch

6. Set the main file path to `app.py`

7. Add your MongoDB connection string in the app's secrets:
   - Go to app settings
   - Click on "Secrets"
   - Add your MongoDB connection string:
```toml
[mongodb]
connection_string = "your_mongodb_connection_string"
```

8. Click "Deploy"

## Environment Variables

- `MONGO_URI`: MongoDB connection string
- `ADMIN_PASSWORD`: Admin user password (default: 'admin123')

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 