import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

const dummyRecipes = [
  {
    id: 1,
    title: 'Classic Spaghetti Bolognese',
    category: 'Quick & Easy',
    description: 'A hearty Italian dish with rich meat sauce.',
    image: 'https://via.placeholder.com/400x250.png?text=Spaghetti',
    rating: 4.5
  },
  {
    id: 2,
    title: 'Healthy Avocado Toast',
    category: 'Healthy',
    description: 'A nutritious snack packed with good fats.',
    image: 'https://via.placeholder.com/400x250.png?text=Avocado+Toast',
    rating: 4.8
  },
  {
    id: 3,
    title: 'Chocolate Lava Cake',
    category: 'Desserts',
    description: 'Warm, gooey chocolate center for indulgence.',
    image: 'https://via.placeholder.com/400x250.png?text=Lava+Cake',
    rating: 4.9
  }
];

const categories = ['Quick & Easy', 'Healthy', 'Desserts'];

const HomePage = () => {
  const [searchTerm, setSearchTerm] = useState('');

  const filteredRecipes = dummyRecipes.filter(recipe =>
    recipe.title.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="space-y-12">
      {/* Hero Section */}
      <div className="bg-cover bg-center h-96 flex flex-col justify-center items-center text-white text-center px-4" style={{ backgroundImage: "url('https://via.placeholder.com/1200x400.png?text=Featured+Recipes')" }}>
        <h1 className="text-4xl md:text-5xl font-bold mb-4">Discover Delicious Recipes</h1>
        <p className="text-lg mb-6">Find meals you'll love and share your own creations.</p>
        <input
          type="text"
          value={searchTerm}
          onChange={e => setSearchTerm(e.target.value)}
          placeholder="Search by name, ingredient or category..."
          className="px-4 py-2 w-full max-w-md rounded-lg text-gray-800"
        />
      </div>

      {/* Featured/Trending Section */}
      <section className="container mx-auto px-4">
        <h2 className="text-2xl font-semibold mb-4">Trending Recipes</h2>
        <div className="grid gap-6 grid-cols-1 sm:grid-cols-2 md:grid-cols-3">
          {filteredRecipes.map(recipe => (
            <Link to={`/recipe/${recipe.id}`} key={recipe.id} className="bg-white rounded-lg shadow hover:shadow-lg overflow-hidden">
              <img src={recipe.image} alt={recipe.title} className="w-full h-48 object-cover" />
              <div className="p-4">
                <h3 className="text-lg font-bold mb-1">{recipe.title}</h3>
                <p className="text-sm text-gray-600 mb-2">{recipe.description}</p>
                <div className="text-yellow-500">{'★'.repeat(Math.round(recipe.rating))}</div>
              </div>
            </Link>
          ))}
        </div>
      </section>

      {/* Categories */}
      <section className="bg-gray-100 py-8">
        <div className="container mx-auto px-4">
          <h2 className="text-2xl font-semibold mb-6">Browse by Category</h2>
          <div className="flex flex-wrap gap-4">
            {categories.map(cat => (
              <div key={cat} className="flex-1 min-w-[150px] bg-white shadow rounded-lg p-4 text-center hover:bg-yellow-50">
                <div className="text-xl font-semibold mb-1">{cat}</div>
                <p className="text-sm text-gray-500">Explore {cat.toLowerCase()} recipes</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Community Section */}
      <section className="container mx-auto px-4">
        <h2 className="text-2xl font-semibold mb-4">What Our Users Say</h2>
        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
          <div className="bg-white rounded-lg p-4 shadow">
            <p className="italic">“This site has completely transformed the way I cook!”</p>
            <div className="text-right mt-2 font-semibold">— Jamie L.</div>
          </div>
          <div className="bg-white rounded-lg p-4 shadow">
            <p className="italic">“I love being able to save my favorite recipes.”</p>
            <div className="text-right mt-2 font-semibold">— Ayesha R.</div>
          </div>
          <div className="bg-white rounded-lg p-4 shadow">
            <p className="italic">“So many great dishes in one place. Highly recommend!”</p>
            <div className="text-right mt-2 font-semibold">— Carlos M.</div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default HomePage;
