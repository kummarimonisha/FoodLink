import React, { useState} from 'react';

function ForgotPasswordPage() {
  const [email, setEmail] = useState("");
  const [resetLink, setResetLink] = useState("");
  const [error, setError] = useState(null);
  const [message, setMessage] = useState(null);
  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage(null);
    setError(null);
  
  // Grab info from backend
  const res = await fetch("http://localhost:5000/api/auth/forgot-password", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email }),
  });

  const data = await res.json();

  if (!res.ok) {
    setError(data.message);
    return;
  }

  setMessage(data.message);

  if (data.reset_link) {
    setResetLink(data.reset_link);
  }
  };

  return (
    <div>
      <h2>Forgot Password</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="email"
          placeholder="Enter your email:"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <button type="submit">Send Reset Link</button>
      </form>

      {resetLink && (
        <div style={{ marginTop: "20px" }}>
          <p><strong>Reset Link:</strong></p>
          <a href={resetLink}>{resetLink}</a>
        </div>
      )}

      {/* Display Changed Successfully or Error messages */}
      {message && <p style={{ color: "green" }}>{message}</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}
    </div>
  );
}

export default ForgotPasswordPage;