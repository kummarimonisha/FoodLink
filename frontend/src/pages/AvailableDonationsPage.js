import React, { useEffect, useState } from "react";
import axios from "axios";

export default function AvailableDonationsPage() {
  const [items, setItems] = useState([]);
  const [message, setMessage] = useState("");

  const token = localStorage.getItem("access_token");
  const role = localStorage.getItem("role");

  useEffect(() => {
    const headers = token ? { Authorization: `Bearer ${token}` } : {};

    axios
      .get("http://localhost:5000/api/donations/available", { headers })
      .then((res) => {
        if (Array.isArray(res.data)) setItems(res.data);
        else {
          console.error('Unexpected response for available donations:', res.data);
          setMessage("Failed to load available donations.");
        }
      })
      .catch((err) => {
        console.error('Error fetching available donations:', err.response || err.message || err);
        setMessage("Failed to load available donations.");
      });
  }, []);

  function requestItem(id) {
    axios
      .patch(
        `http://localhost:5000/api/donations/${id}/claim`,
        {},
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      )
      .then(() => {
        setMessage("You successfully requested this item! 🎉");
        setItems((prev) => prev.filter((item) => item.id !== id));
      })
      .catch(() => {
        setMessage("Someone else already claimed this item.");
      });
  }

  return (
    <div className="page-container">
      <h2>Available Donations</h2>

      {message && <p className="info-msg">{message}</p>}

      {items.length === 0 ? (
        <p>No items available right now.</p>
      ) : (
        items.map((item) => (
          <div key={item.id} className="item-box">
            <h3>{item.title}</h3>
            <p>{item.description}</p>
            <p>Quantity: {item.quantity}</p>
            <p>Expires: {item.expiration_date}</p>

            {role === "recipient" && (
              <button className="btn-primary" onClick={() => requestItem(item.id)}>
                Request Item
              </button>
            )}
          </div>
        ))
      )}
    </div>
  );
}
