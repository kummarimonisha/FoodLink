import { useEffect, useRef } from "react";
import { Navigate } from "react-router-dom";

export default function ProtectedRoute({ children }) {
  const token = localStorage.getItem("access_token");
  const alerted = useRef(false);
  const role = localStorage.getItem("role");
  
  useEffect(() => {
    if (!token && !alerted.current) {
      alert("You need to be logged in to access this page!");
      alerted.current = true;
    }
  }, [token]);

  if (!token) {
    return <Navigate to="/login" replace />;
  }

    if (role !== "admin") {
    return <Navigate to="/" replace />;
  }

  return children;
}