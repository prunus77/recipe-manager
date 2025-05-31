const express = require('express');
const router = express.Router();
const auth = require('../middleware/auth');
const multer = require('multer');
const path = require('path');
const {
  createRecipe,
  getRecipes,
  getRecipe,
  updateRecipe,
  deleteRecipe
} = require('../controllers/recipeController');

// Configure multer for file uploads
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, 'uploads/');
  },
  filename: (req, file, cb) => {
    cb(null, Date.now() + path.extname(file.originalname));
  }
});

const upload = multer({ storage });

// Public routes
router.get('/', getRecipes);
router.get('/:id', getRecipe);

// Protected routes
router.post('/', auth, upload.single('image'), createRecipe);
router.put('/:id', auth, upload.single('image'), updateRecipe);
router.delete('/:id', auth, deleteRecipe);

module.exports = router; 