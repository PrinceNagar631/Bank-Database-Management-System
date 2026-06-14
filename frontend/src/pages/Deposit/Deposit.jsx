import { useEffect, useState } from "react";
import api from "../../api/axios";
import DashboardLayout from "../../layouts/DashboardLayout";
import "../Transfer/Transfer.css";

function Deposit() {
  const [accounts, setAccounts] = useState([]);
  const [accountNo, setAccountNo] = useState("");
  const [amount, setAmount] = useState("");
  const [message, setMessage] = useState("");
  const [submitting, setSubmitting] = useState(false);
  useEffect(() => {
    loadAccounts();
  }, []);

  async function loadAccounts() {
    const res = await api.get("/accounts/my-accounts");
    setAccounts(res.data);
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setSubmitting(true);

    try {
      await api.post("/transactions/deposit", {
        account_no: Number(accountNo),
        amount: Number(amount),
      });

      setMessage("Deposit successful.");
      setAmount("");
    } catch (err) {
      setMessage(
        typeof err.response?.data?.detail === "string"
          ? err.response.data.detail
          : "Deposit failed. Please try again."
      );
      console.error(err);
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <DashboardLayout>
      <div className="page-container">
        <div className="form-card">
          <h1>Deposit Money</h1>
          {message && (
            <div className="success-message">
              {message}
            </div>
          )}
          <form onSubmit={handleSubmit}>
            <label>Account</label>

            <select
              value={accountNo}
              onChange={(e) => setAccountNo(e.target.value)}
              required
            >
              <option value="">Select Account</option>

              {accounts.map((acc) => (
                <option key={acc.account_no} value={acc.account_no}>
                  {acc.account_no}
                </option>
              ))}
            </select>

            <label>Amount</label>

            <input
              type="number"
              value={amount}
              onChange={(e) => setAmount(e.target.value)}
              required
            />

            <button type="submit" disabled={submitting}>
              {submitting ? "Processing..." : "Submit"}
            </button>
          </form>
        </div>
      </div>
    </DashboardLayout>
  );
}

export default Deposit;