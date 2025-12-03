import React, { useState } from "react";

export default function ForgotPasswordPage() {
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState("");

  function handleSubmit(e) {
    e.preventDefault();
    setMessage("If this email exists, password reset instructions were sent.");
  }

  return (
    <div className="page-container">
      <h2>Reset Password</h2>

      <form onSubmit={handleSubmit} className="form-box">
        <label>Enter your email</label>
        <input
          type="email"
          placeholder="example@email.com"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />

        <button className="btn-primary">Send Reset Link</button>
      </form>

      {message && <p className="success-msg">{message}</p>}
    </div>
  );
}
