import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import "./App.css";

// Pages
import HomePage from "./pages/HomePage";
import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";
import ProfilePage from "./pages/ProfilePage";
import EditProfilePage from "./pages/EditProfilePage";
import ForgotPasswordPage from "./pages/ForgotPasswordPage";
import ResetPasswordPage from "./pages/ResetPasswordPage";

import CreateDonationPage from "./pages/CreateDonationPage";
import AvailableDonationsPage from "./pages/AvailableDonationsPage";
import MyDonationsPage from "./pages/MyDonationsPage";
import EditDonationPage from "./pages/EditDonationPage";   // ⭐ NEW
import RequestDonationPage from "./pages/RequestDonationPage";
import FilterDonationsPage from "./pages/FilterDonationsPage";

import AdminDashboardPage from "./pages/AdminDashboardPage";
import RequestsPage from "./pages/RequestsPage";
import AdminUsersPage from "./pages/AdminUsersPage";

// Routes
import ProtectedRoute from "./components/DefinedRoutes/ProtectedRoute";
import AdminRoute from "./components/DefinedRoutes/AdminRoute";

// Components
import Navbar from "./components/Navbar/Navbar";

function App() {
  return (
    <Router>
      <div className="App">
        <Navbar />

        <Routes>
          {/* ---------------------- PUBLIC ROUTES ---------------------- */}
          <Route path="/" element={<HomePage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route path="/forgot-password" element={<ForgotPasswordPage />} />
          <Route path="/reset-password/:token" element={<ResetPasswordPage />} />

          {/* ---------------------- PROTECTED ROUTES ---------------------- */}
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

          {/* ⭐ NEW: Edit Donation Page */}
          <Route
            path="/edit-donation/:id"
            element={
              <ProtectedRoute>
                <EditDonationPage />
              </ProtectedRoute>
            }
          />

          {/* ---------------------- RECIPIENT FEATURES ---------------------- */}

          <Route path="/available-donations" element={<AvailableDonationsPage />} />

          <Route path="/request-donation" element={<RequestDonationPage />} />

          <Route path="/filter-donations" element={<FilterDonationsPage />} />

          <Route
            path="/requests"
            element={
              <ProtectedRoute>
                <RequestsPage />
              </ProtectedRoute>
            }
          />

          {/* ---------------------- ADMIN ONLY ---------------------- */}

          <Route
            path="/admin-dashboard"
            element={
              <AdminRoute>
                <AdminDashboardPage />
              </AdminRoute>
            }
          />

          <Route
            path="/admin-users"
            element={
              <AdminRoute>
                <AdminUsersPage />
              </AdminRoute>
            }
          />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
