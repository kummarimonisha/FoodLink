import { useEffect, useState } from "react";

export default function AdminDashboard() {
  const [items, setItems] = useState([]);

  useEffect(() => {
    fetch("http://localhost:5000/api/donations/pending", {
      headers: {
        Authorization: "Bearer " + localStorage.getItem("access_token"),
      },
    })
      .then((res) => {
        if (!res.ok) {
          throw new Error("Failed to fetch donations");
        }
        return res.json();
      })
      .then((data) => {
        setItems(data);
      })
      .catch((err) => console.error(err));
  }, []);

  function approve(id) {
    fetch(`http://localhost:5000/api/donations/${id}/approve`, {
      method: "POST",
      headers: {
        Authorization: "Bearer " + localStorage.getItem("access_token"),
      },
    }).then(() => {
      setItems((prev) => prev.filter((item) => item.id !== id));
    });
  }

  function reject(id) {
    fetch(`http://localhost:5000/api/donations/${id}/reject`, {
      method: "POST",
      headers: {
        Authorization: "Bearer " + localStorage.getItem("access_token"),
      },
    }).then(() => {
      setItems((prev) => prev.filter((item) => item.id !== id));
    });
  }

  return (
    <div>
      <h1>Admin Dashboard</h1>
      <h2>Pending Items</h2>

      {items.length === 0 && <p>No pending Donations</p>}

      {items.map((item) => (
        <div key={item.id} className="item-box">
          <h3>{item.title}</h3>
          <p>{item.description}</p>
          <p>Expiry: ${item.expiry}</p>

          <button onClick={() => approve(item.id)}>Approve</button>
          <button onClick={() => reject(item.id)}>Reject</button>
        </div>
      ))}
    </div>
  );
}
