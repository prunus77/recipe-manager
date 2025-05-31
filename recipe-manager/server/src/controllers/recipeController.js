const Recipe = require('../models/Recipe');
const cloudinary = require('cloudinary').v2;

// Configure Cloudinary
cloudinary.config({
  cloud_name: process.env.CLOUDINARY_CLOUD_NAME,
  api_key: process.env.CLOUDINARY_API_KEY,
  api_secret: process.env.CLOUDINARY_API_SECRET
});

const createRecipe = async (req, res) => {
  try {
    const { title, description, ingredients, instructions, tags, isPublic, isAnonymous } = req.body;
    let imageUrl = '';
    let cloudinaryId = '';

    if (req.file) {
      const result = await cloudinary.uploader.upload(req.file.path);
      imageUrl = result.secure_url;
      cloudinaryId = result.public_id;
    }

    const recipe = new Recipe({
      title,
      description,
      ingredients,
      instructions,
      tags,
      isPublic,
      isAnonymous,
      imageUrl,
      cloudinaryId,
      author: isAnonymous ? null : req.user._id
    });

    await recipe.save();
    res.status(201).json(recipe);
  } catch (error) {
    res.status(500).json({ message: 'Error creating recipe', error: error.message });
  }
};

const getRecipes = async (req, res) => {
  try {
    const { search, tag } = req.query;
    let query = { isPublic: true };

    if (search) {
      query.$or = [
        { title: { $regex: search, $options: 'i' } },
        { 'ingredients.name': { $regex: search, $options: 'i' } },
        { tags: { $regex: search, $options: 'i' } }
      ];
    }

    if (tag) {
      query.tags = tag;
    }

    const recipes = await Recipe.find(query)
      .populate('author', 'username')
      .sort({ createdAt: -1 });

    res.json(recipes);
  } catch (error) {
    res.status(500).json({ message: 'Error fetching recipes', error: error.message });
  }
};

const getRecipe = async (req, res) => {
  try {
    const recipe = await Recipe.findById(req.params.id)
      .populate('author', 'username');

    if (!recipe) {
      return res.status(404).json({ message: 'Recipe not found' });
    }

    if (!recipe.isPublic && (!req.user || recipe.author.toString() !== req.user._id.toString())) {
      return res.status(403).json({ message: 'Access denied' });
    }

    res.json(recipe);
  } catch (error) {
    res.status(500).json({ message: 'Error fetching recipe', error: error.message });
  }
};

const updateRecipe = async (req, res) => {
  try {
    const recipe = await Recipe.findById(req.params.id);

    if (!recipe) {
      return res.status(404).json({ message: 'Recipe not found' });
    }

    if (recipe.author.toString() !== req.user._id.toString()) {
      return res.status(403).json({ message: 'Access denied' });
    }

    const updates = req.body;
    if (req.file) {
      if (recipe.cloudinaryId) {
        await cloudinary.uploader.destroy(recipe.cloudinaryId);
      }
      const result = await cloudinary.uploader.upload(req.file.path);
      updates.imageUrl = result.secure_url;
      updates.cloudinaryId = result.public_id;
    }

    Object.assign(recipe, updates);
    await recipe.save();

    res.json(recipe);
  } catch (error) {
    res.status(500).json({ message: 'Error updating recipe', error: error.message });
  }
};

const deleteRecipe = async (req, res) => {
  try {
    const recipe = await Recipe.findById(req.params.id);

    if (!recipe) {
      return res.status(404).json({ message: 'Recipe not found' });
    }

    if (recipe.author.toString() !== req.user._id.toString()) {
      return res.status(403).json({ message: 'Access denied' });
    }

    if (recipe.cloudinaryId) {
      await cloudinary.uploader.destroy(recipe.cloudinaryId);
    }

    await recipe.remove();
    res.json({ message: 'Recipe deleted successfully' });
  } catch (error) {
    res.status(500).json({ message: 'Error deleting recipe', error: error.message });
  }
};

module.exports = {
  createRecipe,
  getRecipes,
  getRecipe,
  updateRecipe,
  deleteRecipe
}; 