import { Link } from "react-router-dom";
import './Navbar.css';
export default function Navbar() { //Navbar 
  const token = localStorage.getItem("access_token");


function logout() {
  localStorage.removeItem("access_token");
  localStorage.removeItem("email");     
  localStorage.removeItem("username");
  localStorage.removeItem("role");
  
  // Redirect to login page
  window.location.href = "/login";
}
  return (
    <nav className="navbar">
      <div className="navbar-logo">
        <Link to="/">Foodlink</Link>
      </div>

      <ul className="navbar-links"> 
        <li><Link to="/">Home</Link></li>
        {token ? (
          <>

            {/* If logged in show Profile and Logout Buttons */}
            <li><Link to="/profile">{"Profile"}</Link></li>
            <li><button onClick={logout} className="logout-btn">Logout</button></li>
          </>
        ) : (
          <>
            {/* Otherwise show Login and Register Buttons */}
            <li><Link to="/login">Login</Link></li>
            <li><Link to="/register">Register</Link></li>
          </>
        )}
      </ul>
    </nav>
  );
}