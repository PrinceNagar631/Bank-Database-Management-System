import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../../api/axios";
import DashboardLayout from "../../layouts/DashboardLayout";
import LoadingSpinner from "../../components/LoadingSpinner";
import "./Dashboard.css";

function Dashboard() {
  const [accounts, setAccounts] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    loadAccounts();
  }, []);

  async function loadAccounts() {
    setLoading(true);
    try {
      const res = await api.get("/accounts/my-accounts");
      setAccounts(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  }

  if (loading) {
    return (
      <DashboardLayout>
        <LoadingSpinner />
      </DashboardLayout>
    );
  }

  const totalBalance = accounts.reduce(
    (sum, acc) => sum + Number(acc.balance || 0),
    0
  );

  return (
    <DashboardLayout>
      <h1>Dashboard</h1>

      <div className="summary-grid">
        <div className="summary-card">
          <h3>Total Accounts</h3>
          <h2>{accounts.length}</h2>
        </div>

        <div className="summary-card">
          <h3>Total Balance</h3>
          <h2>₹ {totalBalance.toLocaleString("en-IN")}</h2>
        </div>

        <div
          className="summary-card clickable"
          onClick={() => navigate("/accounts")}
        >
          <h3>My Accounts</h3>
          <p>View all accounts</p>
        </div>

        <div
          className="summary-card clickable"
          onClick={() => navigate("/transfer")}
        >
          <h3>Transfer Money</h3>
          <p>Start a transfer</p>
        </div>
      </div>

      <h2 style={{ marginTop: "30px", marginBottom: "20px" }}>
        Your Accounts
      </h2>

      <div className="account-grid">
        {accounts.map((acc) => (
          <div key={acc.account_no} className="account-card">
            <h3>{acc.account_type}</h3>

            <p>
              <strong>Account Number:</strong>
            </p>
            <p>{acc.account_no}</p>

            <p>
              <strong>Balance:</strong>
            </p>
            <h2>₹ {Number(acc.balance).toLocaleString("en-IN")}</h2>

            <p>
              <strong>Status:</strong> {acc.status}
            </p>
          </div>
        ))}
      </div>
    </DashboardLayout>
  );
}

export default Dashboard;