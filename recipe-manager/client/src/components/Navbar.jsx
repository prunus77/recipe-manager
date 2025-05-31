import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const Navbar = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <nav className="bg-white border-b border-gray-100 sticky top-0 z-50">
      <div className="container mx-auto px-4">
        <div className="flex justify-between items-center h-20">
          <Link to="/" className="flex items-center space-x-2 group">
            <span className="text-3xl font-bold bg-gradient-to-r from-orange-500 to-orange-600 bg-clip-text text-transparent group-hover:from-orange-600 group-hover:to-orange-700 transition-all duration-300">
              RecipeShare
            </span>
          </Link>

          <div className="flex items-center space-x-6">
            <Link 
              to="/" 
              className="text-gray-600 hover:text-orange-600 transition-colors duration-200 font-medium"
            >
              Home
            </Link>
            {user ? (
              <>
                <Link 
                  to="/recipe/new" 
                  className="text-gray-600 hover:text-orange-600 transition-colors duration-200 font-medium"
                >
                  New Recipe
                </Link>
                <Link 
                  to="/profile" 
                  className="text-gray-600 hover:text-orange-600 transition-colors duration-200 font-medium"
                >
                  Profile
                </Link>
                <button
                  onClick={handleLogout}
                  className="bg-orange-500 text-white px-6 py-2 rounded-full hover:bg-orange-600 transition-all duration-300 transform hover:scale-105 shadow-md hover:shadow-lg"
                >
                  Logout
                </button>
              </>
            ) : (
              <>
                <Link 
                  to="/login" 
                  className="text-gray-600 hover:text-orange-600 transition-colors duration-200 font-medium"
                >
                  Login
                </Link>
                <Link
                  to="/register"
                  className="bg-orange-500 text-white px-6 py-2 rounded-full hover:bg-orange-600 transition-all duration-300 transform hover:scale-105 shadow-md hover:shadow-lg"
                >
                  Register
                </Link>
              </>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar; 