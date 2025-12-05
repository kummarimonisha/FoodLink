import React, { useEffect, useState } from "react";
import axios from "axios";
import { useParams } from "react-router-dom";

export default function RequestDonationPage() {
  const { id } = useParams();
  const [donation, setDonation] = useState(null);
  const [message, setMessage] = useState("");
  const token = localStorage.getItem("access_token");

  useEffect(() => {
    axios
      .get("http://localhost:5000/api/donations/available")
      .then((res) => {
        const found = res.data.find((d) => d.id === Number(id));
        setDonation(found);
      });
  }, [id]);

  async function requestDonation() {
    try {
      await axios.post(
        `http://localhost:5000/api/donations/request/${id}`,
        {},
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setMessage("Request sent!");
    } catch {
      setMessage("Error requesting donation");
    }
  }

  if (!donation) return <p>Loading...</p>;

  return (
    <div className="card">
      <h2>{donation.title}</h2>

      <p>{donation.description}</p>
      <p>Quantity: {donation.quantity}</p>
      <p>Status: {donation.status}</p>

      <button className="btn btn-primary" onClick={requestDonation}>
        Request This Food
      </button>

      {message && <p>{message}</p>}
    </div>
  );
}
