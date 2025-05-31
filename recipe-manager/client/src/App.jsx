import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import Navbar from './components/Navbar';
import HomePage from './pages/HomePage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import RecipeForm from './pages/RecipeForm';
import RecipeDetails from './pages/RecipeDetails';
import UserProfile from './pages/UserProfile';

const PrivateRoute = ({ children }) => {
  const { user } = useAuth();
  return user ? children : <Navigate to="/login" />;
};

function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
          <Navbar />
          <main className="container mx-auto px-4 py-8 max-w-7xl">
            <div className="bg-white rounded-xl shadow-lg p-6">
              <Routes>
                <Route path="/" element={<HomePage />} />
                <Route path="/login" element={<LoginPage />} />
                <Route path="/register" element={<RegisterPage />} />
                <Route path="/recipe/:id" element={<RecipeDetails />} />
                <Route
                  path="/recipe/new"
                  element={
                    <PrivateRoute>
                      <RecipeForm />
                    </PrivateRoute>
                  }
                />
                <Route
                  path="/recipe/edit/:id"
                  element={
                    <PrivateRoute>
                      <RecipeForm />
                    </PrivateRoute>
                  }
                />
                <Route
                  path="/profile"
                  element={
                    <PrivateRoute>
                      <UserProfile />
                    </PrivateRoute>
                  }
                />
              </Routes>
            </div>
          </main>
          <footer className="bg-white border-t border-gray-200 py-6 mt-8">
            <div className="container mx-auto px-4 text-center text-gray-600">
              <p>© 2024 RecipeShare. All rights reserved.</p>
            </div>
          </footer>
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;
