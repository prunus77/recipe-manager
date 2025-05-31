const mongoose = require('mongoose');

const recipeSchema = new mongoose.Schema({
  title: {
    type: String,
    required: true,
    trim: true
  },
  description: {
    type: String,
    required: true
  },
  ingredients: [{
    name: String,
    amount: String,
    unit: String
  }],
  instructions: [{
    type: String,
    required: true
  }],
  tags: [{
    type: String,
    enum: ['Quick', 'Spicy', 'Budget-friendly', 'Vegan', 'Vegetarian', 'Gluten-free', 'Dairy-free']
  }],
  imageUrl: {
    type: String,
    default: ''
  },
  cloudinaryId: {
    type: String,
    default: ''
  },
  isPublic: {
    type: Boolean,
    default: true
  },
  author: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User'
  },
  isAnonymous: {
    type: Boolean,
    default: false
  },
  createdAt: {
    type: Date,
    default: Date.now
  },
  updatedAt: {
    type: Date,
    default: Date.now
  }
});

module.exports = mongoose.model('Recipe', recipeSchema); 