import { useEffect, useState } from "react";
import api from "../../api/axios";
import DashboardLayout from "../../layouts/DashboardLayout";
import LoadingSpinner from "../../components/LoadingSpinner";
import "./Transactions.css";

function Transactions() {
  const [accounts, setAccounts] = useState([]);
  const [selectedAccount, setSelectedAccount] = useState("");
  const [transactions, setTransactions] = useState([]);
  const [loading, setLoading] = useState(true);
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

  async function loadTransactions() {
    if (!selectedAccount) return;

    setLoading(true);
    try {
      const res = await api.get(
        `/transactions/history/${selectedAccount}`
      );
      setTransactions(res.data);
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
      <h1>Transaction History</h1>

      <div className="transaction-controls">
        <select
          value={selectedAccount}
          onChange={(e) => setSelectedAccount(e.target.value)}
        >
          <option value="">Select Account</option>

          {accounts.map((acc) => (
            <option
              key={acc.account_no}
              value={acc.account_no}
            >
              {acc.account_no}
            </option>
          ))}
        </select>

        <button onClick={loadTransactions}>
          Load Transactions
        </button>
      </div>

      <table className="transaction-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Type</th>
            <th>Amount</th>
            <th>Balance After</th>
            <th>Date & Time</th>
          </tr>
        </thead>

        <tbody>
          {transactions.map((txn) => (
            <tr key={txn.transaction_id}>
              <td>{txn.transaction_id}</td>

              <td
                className={
                  txn.entry_type === "Credit"
                    ? "credit"
                    : "debit"
                }
              >
                {txn.entry_type}
              </td>

              <td>₹ {Number(txn.amount).toLocaleString("en-IN")}</td>

              <td>₹ {Number(txn.balance_after).toLocaleString("en-IN")}</td>

              <td>{txn.entry_time}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </DashboardLayout>
  );
}

export default Transactions;