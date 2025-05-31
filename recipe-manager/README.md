# Recipe Sharing Application

A full-stack recipe sharing application with user authentication, recipe management, and image upload capabilities.

## Features

- User registration and login with JWT authentication
- Recipe creation, editing, and deletion
- Public and private recipe sharing options
- Anonymous recipe submission
- Tag-based filtering (Quick, Spicy, Budget-friendly, etc.)
- Image upload and preview using Cloudinary
- Search by title, ingredient, or tag
- Responsive design for desktop and mobile

## Prerequisites

- Node.js (v14 or higher)
- MongoDB
- Cloudinary account
- npm or yarn

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd recipe-app
```

2. Install dependencies:
```bash
npm install
```

3. Create a `.env` file in the server directory:
```bash
cd server
cp .env.example .env
```

4. Update the `.env` file with your configuration:
```
PORT=5000
MONGODB_URI=mongodb://localhost:27017/recipe-app
JWT_SECRET=your_jwt_secret_key
CLOUDINARY_CLOUD_NAME=your_cloudinary_cloud_name
CLOUDINARY_API_KEY=your_cloudinary_api_key
CLOUDINARY_API_SECRET=your_cloudinary_api_secret
```

5. Create the uploads directory:
```bash
mkdir server/uploads
```

## Running the Application

1. Start the server:
```bash
npm run dev
```

2. In a new terminal, start the client:
```bash
npm run client
```

Or run both simultaneously:
```bash
npm run dev:full
```

## API Endpoints

### Authentication
- POST /api/users/register - Register a new user
- POST /api/users/login - Login user

### Recipes
- GET /api/recipes - Get all public recipes
- GET /api/recipes/:id - Get a specific recipe
- POST /api/recipes - Create a new recipe (requires authentication)
- PUT /api/recipes/:id - Update a recipe (requires authentication)
- DELETE /api/recipes/:id - Delete a recipe (requires authentication)

## Technologies Used

- Frontend: React, Tailwind CSS
- Backend: Node.js, Express
- Database: MongoDB
- Authentication: JWT
- File Storage: Cloudinary
- Image Upload: Multer

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License.
