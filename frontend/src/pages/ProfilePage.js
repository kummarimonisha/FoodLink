import React from "react";

export default function ProfilePage() {
  const username = localStorage.getItem("username");
  const email = localStorage.getItem("email");
  const role = localStorage.getItem("role");

  return (
    <div className="card" style={{ maxWidth: "600px", margin: "auto" }}>
      <h2>Your Profile</h2>

      <p><strong>Username:</strong> {username}</p>
      <p><strong>Email:</strong> {email}</p>
      <p><strong>Role:</strong> {role}</p>

      <a 
        href="/profile/edit" 
        className="btn btn-secondary" 
        style={{ marginTop: "15px", display: "inline-block" }}
      >
        Edit Profile
      </a>
    </div>
  );
}
