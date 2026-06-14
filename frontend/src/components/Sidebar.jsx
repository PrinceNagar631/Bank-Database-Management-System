import "./Sidebar.css";
import { NavLink, useNavigate } from "react-router-dom";

function Sidebar() {
  const navigate = useNavigate();

  const logout = () => {
    localStorage.removeItem("access_token");
    navigate("/",{ replace: true });
  };

  return (
    <aside className="sidebar">
      <div>
        <h2 className="sidebar-title">Bank Portal</h2>

        <nav className="sidebar-nav">
          <NavLink to="/dashboard">Dashboard</NavLink>
          <NavLink to="/accounts">My Accounts</NavLink>
          <NavLink to="/deposit">Deposit</NavLink>
          <NavLink to="/withdraw">Withdraw</NavLink>
          <NavLink to="/transfer">Transfer</NavLink>
          <NavLink to="/transactions">Transactions</NavLink>
          <NavLink to="/beneficiaries">Beneficiaries</NavLink>
          <NavLink to="/loans">Loans</NavLink>
        </nav>
      </div>

      <button className="logout-btn" onClick={logout}>
        Logout
      </button>
    </aside>
  );
}

export default Sidebar;