import React, {useState} from 'react';

import { useParams } from "react-router-dom";

function ResetPasswordPage() {
  const params = useParams();
  const token = params.token;

  const [password, setPassword] = useState("");
  const [error, setError] = useState(null);

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError(null);

    if (!token) {
      setError("Invalid or missing token.");
      return;
    }
    
    //Try to grab token and new password
    try {
      const res = await fetch("http://localhost:5000/api/auth/reset-password", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": "Bearer " + token
        },
        body: JSON.stringify({ password: password })
      });

      const data = await res.json();

      if (!res.ok) {
        setError(data.error || "Token expired or invalid.");
        return;
      }

      // Success alert
      alert("Password has been reset successfully!");

      // Clear form
      setPassword("");
      setError(null);

    } catch (err) {
      setError("An error occurred. Please try again.");
    }
  };


  return (
  <div style={{ padding: "20px" }}>
    <h2>Reset Your Password</h2>

    {error ? <p style={{ color: "red" }}>{error}</p> : null}

    <form onSubmit={handleSubmit}>
      <input
        type="password"
        placeholder="Enter new password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        required
      />

      <button type="submit">Reset Password</button>
    </form>
  </div>
);
}

export default ResetPasswordPage;