import React, { useState } from 'react';
import RecipeCard from '../components/RecipeCard';
import TagFilter from '../components/TagFilter';

const sampleRecipes = [
  { id: 1, title: 'Spicy Ramen', tags: ['Spicy', 'Quick'], image: 'https://via.placeholder.com/150' },
  { id: 2, title: 'Budget Tacos', tags: ['Budget-friendly'], image: 'https://via.placeholder.com/150' }
];

const tags = ['Quick', 'Spicy', 'Budget-friendly'];

const HomePage = () => {
  const [selectedTag, setSelectedTag] = useState('');

  const filteredRecipes = selectedTag
    ? sampleRecipes.filter(recipe => recipe.tags.includes(selectedTag))
    : sampleRecipes;

  return (
    <div className="p-6">
      <TagFilter tags={tags} selectedTag={selectedTag} onSelectTag={setSelectedTag} />
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {filteredRecipes.map(recipe => (
          <RecipeCard key={recipe.id} recipe={recipe} />
        ))}
      </div>
    </div>
  );
};

export default HomePage;
