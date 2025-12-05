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
            {/* Otherwise show Login and Register Buttons */}
            <li><Link to="/login">Login</Link></li>
            <li><Link to="/register">Register</Link></li>
          </>
        )}

        {token && (
          <>
            {role === "donor" && (
              <>
                <li><Link to="/create-donation">Create Donation</Link></li>
                <li><Link to="/my-donations">My Donations</Link></li>
              </>
            )}

            {role === "recipient" && (
              <>
                <li><Link to="/available-donations">Available</Link></li>
                <li><Link to="/filter-donations">Filter</Link></li>
              </>
            )}

            {role === "admin" && (
              <>
                <li><Link to="/available-donations">Available</Link></li>
                {/* Later add admin features */}
              </>
            )}

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
