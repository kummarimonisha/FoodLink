import React, {useState} from 'react';
import axios from 'axios';
function RegisterPage() {
      const [email, setEmail] = useState("");
      const [username, setUsername] = useState("");
      const [password, setPassword] = useState("");
      const [role, setRole] = useState("recipient");
      const [message, setMessage] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage("");

    try {
      const res = await axios.post("http://localhost:5000/api/auth/register", {
        email,
        username,
        password,
        role,
      });

      setMessage("Registration successful! Please proceed to login page!");
    } 
    catch (err) {
      setMessage(err.response?.data?.msg || "Error registering user");
    }
  };
    
  return (
    <div className="register-container">
      <form onSubmit={handleSubmit}>
        <h2>Register</h2>

        <input
          type="email"
          placeholder="Email"
          onChange={(e) => setEmail(e.target.value)}
          value={email}
        />

        <input
          type="username"
          placeholder="Username"
          onChange={(e) => setUsername(e.target.value)}
          value={username}
        />

        <input
          type="password"
          placeholder="Password"
          onChange={(e) => setPassword(e.target.value)}
          value={password}
        />

        <select value={role} onChange={(e) => setRole(e.target.value)}>
          <option value="recipient">Recipient</option>
          <option value="donor">Donor</option>
          <option value="admin">Admin</option>
        </select>

        <button type="submit">Create Account</button>

        {message && <p>{message}</p>}
      </form>
    </div>
  );
}

export default RegisterPage;