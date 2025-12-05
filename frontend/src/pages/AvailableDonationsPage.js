import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";

export default function AvailableDonationsPage() {
  const [donations, setDonations] = useState([]);

  useEffect(() => {
    fetch("http://localhost:5000/api/donations/available")
      .then((res) => res.json())
      .then((data) => setDonations(data))
      .catch((err) => console.error(err));
  }, []);

  return (
    <div className="card">
      <h2>Available Donations</h2>

      {donations.length === 0 ? (
        <p>No donations available right now.</p>
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
              <Link to={`/donation/${d.id}`} style={{ fontSize: "18px", fontWeight: "600" }}>
                {d.title}
              </Link>

              <p>{d.description}</p>
              <p><strong>Category:</strong> {d.category}</p>
              <p><strong>Quantity:</strong> {d.quantity}</p>
              <p><strong>Status:</strong> {d.status}</p>

              <Link to={`/donation/${d.id}`}>
                <button className="btn btn-primary">View / Request</button>
              </Link>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
