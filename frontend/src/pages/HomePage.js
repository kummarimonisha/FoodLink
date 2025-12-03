import React, { useEffect, useState } from "react";

export default function HomePage() {
  const [message, setMessage] = useState("");

  useEffect(() => {
    fetch("http://localhost:5000/api/health")
      .then((r) => r.json())
      .then((d) => setMessage(d.message));
  }, []);

  return (
    <div className="card">
      <h1>FoodLink</h1>
      <p>{message}</p>
      <p>Welcome to the platform! Use the navbar to explore your options.</p>
    </div>
  );
}
