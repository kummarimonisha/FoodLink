import React, {useEffect, useState} from 'react';

function HomePage() {
      const [message, setMessage] = useState("");
    
      useEffect(() => {
        fetch("http://localhost:5000/api/health")
        .then(response => response.json())
        .then(data => setMessage(data.message))
        .catch(error => console.error('Error:', error));
    
      })
    
  return (
    <div>
      <h1>{message}</h1>
      <p>This is also the front end running.</p>
    </div>
  );
}

export default HomePage;