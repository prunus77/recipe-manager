import React from 'react';

const RecipeCard = ({ recipe }) => {
  return (
    <div className="border p-4 rounded shadow-md">
      <img src={recipe.image} alt={recipe.title} className="w-full h-40 object-cover rounded" />
      <h3 className="text-lg font-semibold mt-2">{recipe.title}</h3>
      <p className="text-sm text-gray-600">{recipe.tags.join(', ')}</p>
    </div>
  );
};