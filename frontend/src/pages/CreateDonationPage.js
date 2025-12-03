import React, { useState } from "react";
import axios from "axios";

export default function CreateDonationPage() {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [category, setCategory] = useState("non_perishable");
  const [quantity, setQuantity] = useState(1);
  const [message, setMessage] = useState("");

  const token = localStorage.getItem("access_token");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage("");

    try {
      await axios.post(
        "http://localhost:5000/api/donations/",
        { title, description, category, quantity },
        { headers: { Authorization: `Bearer ${token}` } }
      );

      setMessage("Donation created successfully!");
      setTitle("");
      setDescription("");
      setQuantity(1);
    } catch (err) {
      setMessage("Error creating donation");
    }
  };

    // Shared styles for perfect alignment
    const rowStyle = {
      display: "grid",
      gridTemplateColumns: "150px 1fr",
      alignItems: "center",
      marginBottom: "15px",
      width: "100%",
    };

    const labelStyle = {
      width: "150px",      // keeps all labels aligned
      textAlign: "right",  // aligns last letter of each label
      marginRight: "15px",
      fontWeight: 500,
    };

    const inputStyle = {
      width: "260px",      // keeps input widths consistent
      padding: "6px",
    };

    return (
    <div
      className="card"
      style={{
        maxWidth: "650px",
        margin: "auto",
        textAlign: "center",
      }}
    >
      <h2>Create Donation</h2>

      <form
        onSubmit={handleSubmit}
        style={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          marginTop: "10px",
        }}
      >
        <>
            {/* Title */}
            <div style={rowStyle}>
              <label style={labelStyle}>Title:</label>
              <input
                type="text"
                value={title}
                placeholder="Canned Food"
                onChange={(e) => setTitle(e.target.value)}
                style={inputStyle}
              />
            </div>

            {/* Description */}
            <div style={rowStyle}>
              <label style={labelStyle}>Description:</label>
              <textarea
                value={description}
                placeholder="Short description"
                onChange={(e) => setDescription(e.target.value)}
                style={{ ...inputStyle, minHeight: "90px" }}
              ></textarea>
            </div>

            {/* Category */}
            <div style={rowStyle}>
              <label style={labelStyle}>Category:</label>
              <select
                value={category}
                onChange={(e) => setCategory(e.target.value)}
                style={inputStyle}
              >
                <option value="non_perishable">Non-Perishable</option>
                <option value="prepared_food">Prepared Food</option>
                <option value="produce">Produce</option>
              </select>
            </div>

            {/* Quantity */}
            <div style={rowStyle}>
              <label style={labelStyle}>Quantity:</label>
              <input
                type="number"
                min="1"
                value={quantity}
                onChange={(e) => setQuantity(e.target.value)}
                style={{ ...inputStyle, width: "120px" }}
              />
            </div>

            <button
              className="btn btn-primary"
              type="submit"
              style={{ marginTop: "10px" }}
            >
              Submit Donation
            </button>

            {message && <p style={{ marginTop: "12px" }}>{message}</p>}
          </>
      </form>
    </div>
  );
}
