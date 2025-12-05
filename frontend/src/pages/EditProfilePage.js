import React, { useState } from "react";

export default function EditProfilePage() {
  const [username, setUsername] = useState(localStorage.getItem("username") || "");
  const [email, setEmail] = useState(localStorage.getItem("email") || "");
  const [message, setMessage] = useState("");

  function handleSubmit(e) {
    e.preventDefault();

    fetch("http://localhost:5000/api/profile/update", {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("access_token")}`
      },
      body: JSON.stringify({ username, email })
    })
      .then((res) => res.json())
      .then(() => {
        localStorage.setItem("username", username);
        localStorage.setItem("email", email);
        setMessage("Profile updated successfully!");
      })
      .catch(() => setMessage("Error updating profile."));
  }

  return (
    <div className="page-container">
      <h2>Edit Profile</h2>

      <form onSubmit={handleSubmit} className="form-box">
        <label>Username</label>
        <input value={username} onChange={(e) => setUsername(e.target.value)} />

        <label>Email</label>
        <input value={email} onChange={(e) => setEmail(e.target.value)} />

        <button className="btn-primary">Save Changes</button>
      </form>

      {message && <p className="success-msg">{message}</p>}
    </div>
  );
}
