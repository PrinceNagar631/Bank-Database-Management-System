import { useLocation } from "react-router-dom";

function Topbar() {
  const location = useLocation();

  const titles = {
    "/dashboard": "Dashboard",
    "/accounts": "My Accounts",
    "/deposit": "Deposit Money",
    "/withdraw": "Withdraw Money",
    "/transfer": "Transfer Money",
    "/transactions": "Transaction History",
    "/beneficiaries": "Beneficiaries",
    "/register": "Register",
  };

  return (
    <header
      style={{
        height: "70px",
        background: "#ffffff",
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        padding: "0 30px",
        borderBottom: "1px solid #e5e7eb",
      }}
    >
      <h2>{titles[location.pathname] || "Bank Portal"}</h2>

      <span>Secure Banking System</span>
    </header>
  );
}

export default Topbar;