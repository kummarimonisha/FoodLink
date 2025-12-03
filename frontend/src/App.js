import React from 'react'; 
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import './App.css';

// Pages
import HomePage from './pages/HomePage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import ProfilePage from './pages/ProfilePage';
import EditProfilePage from './pages/EditProfilePage';
import ForgotPasswordPage from './pages/ForgotPasswordPage';

import CreateDonationPage from './pages/CreateDonationPage';
import AvailableDonationsPage from './pages/AvailableDonationsPage';
import MyDonationsPage from './pages/MyDonationsPage';
import RequestDonationPage from './pages/RequestDonationPage';
import FilterDonationsPage from './pages/FilterDonationsPage';

import ProtectedRoute from './pages/ProtectedRoute';

// Components
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
          <Route path="/forgot-password" element={<ForgotPasswordPage />} />

          <Route 
            path="/profile" 
            element={
              <ProtectedRoute>
                <ProfilePage />
              </ProtectedRoute>
            } 
          />

          <Route 
            path="/profile/edit" 
            element={
              <ProtectedRoute>
                <EditProfilePage />
              </ProtectedRoute>
            } 
          />

          <Route 
            path="/create-donation" 
            element={
              <ProtectedRoute>
                <CreateDonationPage />
              </ProtectedRoute>
            } 
          />

          <Route 
            path="/my-donations" 
            element={
              <ProtectedRoute>
                <MyDonationsPage />
              </ProtectedRoute>
            } 
          />

          <Route 
            path="/available-donations" 
            element={<AvailableDonationsPage />} 
          />

          <Route 
            path="/request-donation" 
            element={<RequestDonationPage />} 
          />

          <Route 
            path="/filter-donations" 
            element={<FilterDonationsPage />} 
          />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
