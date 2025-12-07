import React, { useEffect, useState } from "react";
import axios from "axios";

export default function RequestsPage() {
  const [requests, setRequests] = useState([]);
  const token = localStorage.getItem("access_token");

  useEffect(() => {
    axios
      .get("http://localhost:5000/api/requests/mine", {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then((res) => setRequests(res.data))
      .catch(() => console.log("Failed to load requests"));
  }, [token]);

  return (
    <div className="page-container">
      <h2>My Requests</h2>

      {requests.length === 0 ? (
        <p>You haven't requested anything yet.</p>
      ) : (
        requests.map((r) => (
          <div key={r.id} className="item-box">
            <h3>{r.title}</h3>
            <p>Status: {r.status}</p>
          </div>
        ))
      )}
    </div>
  );
}
