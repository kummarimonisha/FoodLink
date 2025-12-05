import React, { useEffect, useState } from "react";

export default function FilterDonationsPage() {
  const [donations, setDonations] = useState([]);
  const [filtered, setFiltered] = useState([]);
  const [category, setCategory] = useState("all");

  useEffect(() => {
    fetch("http://localhost:5000/api/donations/available")
      .then((res) => res.json())
      .then((data) => {
        setDonations(data);
        setFiltered(data);
      });
  }, []);

  function filterList() {
    if (category === "all") setFiltered(donations);
    else setFiltered(donations.filter((d) => d.category === category));
  }

  return (
    <div className="card">
      <h2>Filter Donations</h2>

      <label>Category</label>
      <select value={category} onChange={(e) => setCategory(e.target.value)}>
        <option value="all">All</option>
        <option value="non_perishable">Non-Perishable</option>
        <option value="prepared_food">Prepared Food</option>
        <option value="produce">Produce</option>
      </select>

      <button className="btn btn-primary" onClick={filterList}>
        Apply Filter
      </button>

      <ul style={{ marginTop: "20px", listStyle: "none", padding: 0 }}>
        {filtered.map((d) => (
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
            <strong>{d.title}</strong> — {d.category}
            <p>{d.description}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}
