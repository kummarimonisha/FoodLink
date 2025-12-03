import React, { useEffect, useState } from "react";
import axios from "axios";

export default function MyDonationsPage() {
  const [donations, setDonations] = useState([]);
  const token = localStorage.getItem("access_token");

  useEffect(() => {
    axios
      .get("http://localhost:5000/api/donations/mine", {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then((res) => setDonations(res.data));
  }, [token]);

  return (
    <div className="card">
      <h2>My Donations</h2>

      {donations.length === 0 ? (
        <p>You don’t have any donations yet.</p>
      ) : (
        <ul style={{ listStyle: "none", padding: 0 }}>
          {donations.map((d) => (
            <li
              key={d.id}
              style={{
                background: "#fff",
                padding: "15px",
                borderRadius: "10px",
                marginBottom: "15px",
                boxShadow: "0 2px 8px rgba(0,0,0,0.05)",
              }}
            >
              <strong>{d.title}</strong>
              <p>{d.description}</p>
              <p>Quantity: {d.quantity}</p>
              <p>Status: {d.status}</p>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
