import React from 'react';
import { Link } from 'react-router-dom';

const Header = () => {
  return (
    <header className="bg-primary-700 text-white shadow-lg">
      <div className="container mx-auto px-4 py-6">
        <div className="flex items-center justify-between">
          <Link to="/" className="flex items-center space-x-3">
            <div className="text-3xl font-bold">
              Career Recommendation System
            </div>
          </Link>
          <nav className="hidden md:flex space-x-6">
            <Link to="/" className="hover:text-primary-200 transition-colors">
              Home
            </Link>
            <Link to="/assessment" className="hover:text-primary-200 transition-colors">
              Start Assessment
            </Link>
          </nav>
        </div>
        <p className="text-primary-100 text-sm mt-2">
          Defence & Civil Services Career Guidance
        </p>
      </div>
    </header>
  );
};

export default Header;
