import React, { useEffect, useState } from "react";

export default function AdminUsersPage() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [deactivatingId, setDeactivatingId] = useState(null);

  const fetchUsers = () => {
    const token = localStorage.getItem("access_token");
    setLoading(true);
    setError("");

    // auth blueprint is mounted at /api/auth on the backend
    const url = "http://localhost:5000/api/auth/admin/users";
    const headers = token ? { Authorization: `Bearer ${token}` } : {};

    fetch(url, { headers })
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.json();
      })
      .then((data) => {
        // Expecting an array of users: [{ id, username, email, role }, ...]
        setUsers(Array.isArray(data) ? data : []);
      })
      .catch((err) => {
        console.error(err);
        setError("Failed to load users.");
      })
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchUsers();
  }, []);

  const handleDeactivate = async (userId) => {
    if (!window.confirm("Are you sure you want to deactivate this user?")) {
      return;
    }

    const token = localStorage.getItem("access_token");
    setDeactivatingId(userId);

    try {
      const res = await fetch(
        `http://localhost:5000/api/auth/admin/users/${userId}/deactivate`,
        {
          method: "PATCH",
          headers: {
            ...(token ? { Authorization: `Bearer ${token}` } : {}),
            "Content-Type": "application/json",
          },
        }
      );

      if (!res.ok) throw new Error(`HTTP ${res.status}`);

      // Refetch users after deactivation
      fetchUsers();
    } catch (err) {
      console.error(err);
      alert("Failed to deactivate user.");
    } finally {
      setDeactivatingId(null);
    }
  };

  return (
    <div className="page-container" style={{ padding: 24 }}>
      <h2>Manage Users</h2>

      {loading && <p>Loading users…</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}

      {!loading && !error && (
        <div style={{ overflowX: "auto" }}>
          <table style={{ width: "100%", borderCollapse: "collapse" }}>
            <thead>
              <tr>
                <th style={{ textAlign: "left", padding: "8px", borderBottom: "1px solid #ddd" }}>Username</th>
                <th style={{ textAlign: "left", padding: "8px", borderBottom: "1px solid #ddd" }}>Email</th>
                <th style={{ textAlign: "left", padding: "8px", borderBottom: "1px solid #ddd" }}>Role</th>
                <th style={{ textAlign: "left", padding: "8px", borderBottom: "1px solid #ddd" }}>Actions</th>
              </tr>
            </thead>
            <tbody>
              {users.length === 0 && (
                <tr>
                  <td colSpan={4} style={{ padding: 12 }}>No users found.</td>
                </tr>
              )}

              {users.map((u) => (
                <tr key={u.id || u.email}>
                  <td style={{ padding: 8, borderBottom: "1px solid #f2f2f2" }}>{u.username}</td>
                  <td style={{ padding: 8, borderBottom: "1px solid #f2f2f2" }}>{u.email}</td>
                  <td style={{ padding: 8, borderBottom: "1px solid #f2f2f2" }}>{u.role}</td>
                  <td style={{ padding: 8, borderBottom: "1px solid #f2f2f2" }}>
                    <button
                      onClick={() => handleDeactivate(u.id)}
                      disabled={deactivatingId === u.id}
                      style={{
                        padding: "6px 12px",
                        backgroundColor: "#dc3545",
                        color: "white",
                        border: "none",
                        borderRadius: "4px",
                        cursor: deactivatingId === u.id ? "not-allowed" : "pointer",
                        opacity: deactivatingId === u.id ? 0.6 : 1,
                      }}
                    >
                      {deactivatingId === u.id ? "Deactivating…" : "Deactivate"}
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
