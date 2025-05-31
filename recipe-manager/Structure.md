project-root/
├── client/                         # React Frontend
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── RecipeCard.jsx
│   │   │   └── TagFilter.jsx
│   │   ├── pages/
│   │   │   └── HomePage.jsx
│   │   ├── App.js
│   │   └── index.js
│   ├── .env
│   └── package.json
│
├── server/                        # Node.js Backend
│   ├── controllers/
│   │   └── recipeController.js
│   ├── models/
│   │   └── Recipe.js
│   ├── routes/
│   │   └── recipeRoutes.js
│   ├── middleware/
│   │   └── authMiddleware.js
│   ├── config/
│   │   └── db.js
│   ├── server.js
│   ├── .env
│   └── package.json
│
├── README.md
└── .gitignore