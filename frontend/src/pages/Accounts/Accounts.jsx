import { useEffect, useState } from "react";
import api from "../../api/axios";
import DashboardLayout from "../../layouts/DashboardLayout";
import LoadingSpinner from "../../components/LoadingSpinner";
import "./Accounts.css";

function Accounts() {
  const [accounts, setAccounts] = useState([]);
  const [loading, setLoading] = useState(true);
  useEffect(() => {
    fetchAccounts();
  }, []);

  async function fetchAccounts() {
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

  return (
    <DashboardLayout>
      <h1>My Accounts</h1>

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

export default Accounts;