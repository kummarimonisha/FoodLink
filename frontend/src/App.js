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

import ProtectedRoute from './components/DefinedRoutes/ProtectedRoute';
import ResetPasswordPage from './pages/ResetPasswordPage';

// Components
import Navbar from "./components/Navbar/Navbar";
import AdminDashboardPage from './pages/AdminDashboardPage';
import AdminRoute from './components/DefinedRoutes/AdminRoute';

function App() {
  return (
    <Router>
      <div className="App">
        <Navbar />

        <Routes>
          {/* Routes*/}
          <Route path="/" element={<HomePage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route path="/profile" element={
            <ProtectedRoute>
            <ProfilePage /> {/* Protected so can't be accessed without being logged in */}
            </ProtectedRoute>
            } />
        <Route path="/forgot-password" element={<ForgotPasswordPage />} />
        <Route path="/reset-password/:token" element={<ResetPasswordPage />} />
        <Route path="/admin-dashboard" element={
            <AdminRoute>
            <AdminDashboardPage /> {/* Protected so can't be accessed without being logged in */}
            </AdminRoute>
        } />

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
