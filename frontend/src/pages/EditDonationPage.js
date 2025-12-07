import React, { useEffect, useState } from "react";
import axios from "axios";
import { useParams, useNavigate } from "react-router-dom";

export default function EditDonationPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const token = localStorage.getItem("access_token");

  const [donation, setDonation] = useState(null);
  const [message, setMessage] = useState("");

  // Fetch current donation data
  useEffect(() => {
    axios
      .get("http://localhost:5000/api/donations/mine", {
        headers: { Authorization: `Bearer ${token}` }
      })
      .then((res) => {
        const found = res.data.find((d) => d.id === Number(id));
        setDonation(found);
      })
      .catch(() => setMessage("Failed to load donation"));
  }, [id, token]);

  function handleSubmit(e) {
    e.preventDefault();
    setMessage("");

    axios
      .patch(
        `http://localhost:5000/api/donations/${id}`,
        {
          title: donation.title,
          description: donation.description,
          quantity: donation.quantity,
          category: donation.category
        },
        { headers: { Authorization: `Bearer ${token}` } }
      )
      .then(() => {
        setMessage("Donation updated successfully!");
        setTimeout(() => navigate("/my-donations"), 1200);
      })
      .catch(() => setMessage("Error updating donation"));
  }

  if (!donation) return <p>Loading...</p>;

  return (
    <div className="card" style={{ maxWidth: "650px", margin: "auto" }}>
      <h2>Edit Donation</h2>

      <form onSubmit={handleSubmit}>
        <label>Title</label>
        <input
          type="text"
          value={donation.title}
          onChange={(e) =>
            setDonation({ ...donation, title: e.target.value })
          }
        />

        <label>Description</label>
        <textarea
          value={donation.description}
          onChange={(e) =>
            setDonation({ ...donation, description: e.target.value })
          }
        />

        <label>Quantity</label>
        <input
          type="number"
          value={donation.quantity}
          onChange={(e) =>
            setDonation({ ...donation, quantity: e.target.value })
          }
        />

        <label>Category</label>
        <select
          value={donation.category}
          onChange={(e) =>
            setDonation({ ...donation, category: e.target.value })
          }
        >
          <option value="non_perishable">Non-Perishable</option>
          <option value="prepared_food">Prepared Food</option>
          <option value="produce">Produce</option>
        </select>

        <button
          className="btn btn-primary"
          type="submit"
          style={{ marginTop: "15px" }}
        >
          Save Changes
        </button>

        {message && <p style={{ marginTop: "10px" }}>{message}</p>}
      </form>
    </div>
  );
}
