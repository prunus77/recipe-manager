import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { useAuth } from '../context/AuthContext';

const UserProfile = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [recipes, setRecipes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    if (!user) {
      navigate('/login');
      return;
    }

    const fetchUserRecipes = async () => {
      try {
        const response = await axios.get('http://localhost:5000/api/recipes/user');
        setRecipes(response.data);
      } catch (error) {
        setError('Failed to load your recipes');
      } finally {
        setLoading(false);
      }
    };

    fetchUserRecipes();
  }, [user, navigate]);

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center mt-8">
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded-lg max-w-md mx-auto">
          {error}
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto">
      <div className="bg-white rounded-xl shadow-lg p-8 mb-8">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h1 className="text-3xl font-bold text-gray-800 mb-2">Your Profile</h1>
            <div className="space-y-1">
              <p className="text-gray-600">
                <span className="font-medium">Username:</span> {user.username}
              </p>
              <p className="text-gray-600">
                <span className="font-medium">Email:</span> {user.email}
              </p>
            </div>
          </div>
          <button
            onClick={() => navigate('/recipe/new')}
            className="px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors shadow-sm"
          >
            Create New Recipe
          </button>
        </div>
      </div>

      <div className="bg-white rounded-xl shadow-lg p-8">
        <h2 className="text-2xl font-bold text-gray-800 mb-6">Your Recipes</h2>
        {recipes.length === 0 ? (
          <div className="text-center py-12">
            <p className="text-gray-600 mb-4">You haven't created any recipes yet.</p>
            <button
              onClick={() => navigate('/recipe/new')}
              className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors"
            >
              Create Your First Recipe
            </button>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {recipes.map(recipe => (
              <div
                key={recipe._id}
                className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow"
              >
                {recipe.imageUrl && (
                  <div className="relative h-48">
                    <img
                      src={recipe.imageUrl}
                      alt={recipe.title}
                      className="w-full h-full object-cover"
                    />
                    <div className="absolute inset-0 bg-gradient-to-t from-black/50 to-transparent"></div>
                  </div>
                )}
                <div className="p-6">
                  <h3 className="text-xl font-semibold text-gray-800 mb-2">{recipe.title}</h3>
                  <div className="flex flex-wrap gap-2 mb-4">
                    {recipe.tags.map(tag => (
                      <span
                        key={tag}
                        className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm font-medium"
                      >
                        {tag}
                      </span>
                    ))}
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600">
                      {recipe.isPublic ? 'Public' : 'Private'}
                    </span>
                    <button
                      onClick={() => navigate(`/recipe/edit/${recipe._id}`)}
                      className="text-blue-500 hover:text-blue-600 transition-colors"
                    >
                      Edit Recipe
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default UserProfile; 