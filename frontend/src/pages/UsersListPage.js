import React, { useEffect, useState } from "react";
import axios from "axios";

export default function AdminUsersPage() {
  const [users, setUsers] = useState([]);
  const token = localStorage.getItem("access_token");

  useEffect(() => {
    axios
      .get("http://localhost:5000/api/admin/users", {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then((res) => setUsers(res.data))
      .catch((err) => console.error(err));
  }, [token]);

  function toggleUser(id, currentStatus) {
    const endpoint = currentStatus
      ? `/api/admin/users/${id}/deactivate`
      : `/api/admin/users/${id}/activate`;

    axios
      .patch(`http://localhost:5000${endpoint}`, {}, {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then(() => {
        setUsers((prev) =>
          prev.map((u) =>
            u.id === id ? { ...u, active: !currentStatus } : u
          )
        );
      })
      .catch((err) => console.error(err));
  }

  return (
    <div className="page-container">
      <h2>Manage Users</h2>

      {users.length === 0 ? (
        <p>No users found.</p>
      ) : (
        users.map((u) => (
          <div key={u.id} className="item-box">
            <h3>{u.username}</h3>
            <p>Email: {u.email}</p>
            <p>Role: {u.role}</p>
            <p>Status: {u.active ? "Active" : "Inactive"}</p>

            <button
              className="btn-primary"
              onClick={() => toggleUser(u.id, u.active)}
            >
              {u.active ? "Deactivate" : "Activate"}
            </button>
          </div>
        ))
      )}
    </div>
  );
}
