import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import './App.css';
import HomePage from './pages/HomePage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import ProfilePage  from './pages/ProfilePage';
import ProtectedRoute from './pages/ProtectedRoute';

import Navbar from "./components/Navbar/Navbar";

function App() {

  return (
      <Router>
      <div className="App">
        <Navbar />
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route path="/profile" element={
            <ProtectedRoute>
            <ProfilePage />
            </ProtectedRoute>
            } />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
