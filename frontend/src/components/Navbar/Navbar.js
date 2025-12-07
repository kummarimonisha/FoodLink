import { Link } from "react-router-dom";
import './Navbar.css';

export default function Navbar() {
  const token = localStorage.getItem("access_token");
  const role = localStorage.getItem("role");

  function logout() {
    localStorage.removeItem("access_token");
    localStorage.removeItem("email");
    localStorage.removeItem("username");
    localStorage.removeItem("role");

    window.location.href = "/login";
  }

  return (
    <nav className="navbar">
      <div className="navbar-logo">
        <Link to="/">FoodLink</Link>
      </div>

      <ul className="navbar-links"> 
        <li><Link to="/">Home</Link></li>

        {!token && (
          <>
            <li><Link to="/login">Login</Link></li>
            <li><Link to="/register">Register</Link></li>
          </>
        )}

        {token && (
          <>
            {/* Donor links */}
            {role === "donor" && (
              <>
                <li><Link to="/create-donation">Create Donation</Link></li>
                <li><Link to="/my-donations">My Donations</Link></li>
              </>
            )}

            {/* Recipient links */}
            {role === "recipient" && (
              <>
                <li><Link to="/available-donations">Available</Link></li>
                <li><Link to="/filter-donations">Filter</Link></li>
              </>
            )}

            {/* Admin links */}
            {role === "admin" && (
              <>
                <li><Link to="/available-donations">Available</Link></li>
                <li><Link to="/admin-users">Manage Users</Link></li>
                <li><Link to="/admin-dashboard">Admin Dashboard</Link></li>
              </>
            )}

            {/* NEW Requests tab (for demo purposes) */}
            <li><Link to="/requests">Requests</Link></li>

            <li><Link to="/profile">Profile</Link></li>

            <li>
              <button onClick={logout} className="logout-btn">Logout</button>
            </li>
          </>
        )}
      </ul>
    </nav>
  );
}
