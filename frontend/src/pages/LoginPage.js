import React, { useState } from "react";
import axios from "axios";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");

    try {
      const res = await axios.post("http://localhost:5000/api/auth/login", {
        email,
        password,
      });

      localStorage.setItem("access_token", res.data.access_token);
      localStorage.setItem("email", res.data.user.email);
      localStorage.setItem("username", res.data.user.username);
      localStorage.setItem("role", res.data.user.role);

      window.location.href = "/profile";
    } catch (err) {
      setError("Invalid email or password");
    }
  }

  return (
    <div className="card" style={{ maxWidth: "450px", margin: "auto" }}>
      <h2>Login</h2>

      <form onSubmit={handleSubmit}>
        <label>Email</label>
        <input
          type="email"
          placeholder="Enter your email"
          onChange={(e) => setEmail(e.target.value)}
          style={{ display: "block", width: "100%" }}
        />

        <label>Password</label>
        <input
          type="password"
          placeholder="Enter your password"
          onChange={(e) => setPassword(e.target.value)}
          style={{ display: "block", width: "100%" }}
        />

        {error && <p style={{ color: "red", marginTop: "8px" }}>{error}</p>}

        <button
          className="btn btn-primary"
          type="submit"
          style={{ marginTop: "12px" }}
        >
          Login
        </button>
      </form>

      <p style={{ marginTop: "12px" }}>
        <a href="/forgot-password" className="small-link">
          Forgot Password?
        </a>
      </p>

      <p style={{ marginTop: "5px" }}>
        Don’t have an account?{" "}
        <a href="/register" className="small-link">
          Register here
        </a>
      </p>
    </div>
  );
}
