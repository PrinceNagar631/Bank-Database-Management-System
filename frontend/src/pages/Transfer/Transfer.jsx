import { useEffect, useState } from "react";
import api from "../../api/axios";
import DashboardLayout from "../../layouts/DashboardLayout";
import "./Transfer.css";

function Transfer() {
  const [accounts, setAccounts] = useState([]);
  const [message, setMessage] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [form, setForm] = useState({
    from_account: "",
    to_account: "",
    amount: "",
  });

  useEffect(() => {
    fetchAccounts();
  }, []);

  async function fetchAccounts() {
    try {
      const res = await api.get("/accounts/my-accounts");
      setAccounts(res.data);
    } catch (err) {
      console.error(err);
    }
  }

  async function handleSubmit(e) {
    if (!window.confirm("Do you want to proceed with this transfer?")) {
      return;
    }

    if (
      !form.from_account ||
      !form.to_account ||
      !form.amount ||
      Number(form.amount) <= 0
    ) {
      setMessage("Please enter valid details.");
      return;
    }

    if (Number(form.from_account) === Number(form.to_account)) {
      setMessage("Source and destination accounts cannot be the same.");
      return;
    }

    e.preventDefault();
    setSubmitting(true);

    try {
      await api.post("/transactions/transfer", {
        from_account: Number(form.from_account),
        to_account: Number(form.to_account),
        amount: Number(form.amount),
      });

      setMessage("Transfer completed successfully.");
      fetchAccounts();

      setForm({
        from_account: "",
        to_account: "",
        amount: "",
      });
    } catch (err) {
      setMessage(
        typeof err.response?.data?.detail === "string"
          ? err.response.data.detail
          : "Transfer failed. Please try again."
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
          <h1>Transfer Money</h1>

          {message && (
            <div className="success-message">
              {message}
            </div>
          )}

          <form onSubmit={handleSubmit}>
            <label>From Account</label>
            <select
              value={form.from_account}
              onChange={(e) =>
                setForm({ ...form, from_account: e.target.value })
              }
              required
            >
              <option value="">Select Account</option>

              {accounts.map((acc) => (
                <option key={acc.account_no} value={acc.account_no}>
                  {acc.account_no} ({acc.account_type})
                </option>
              ))}
            </select>

            <label>To Account Number</label>
            <input
              type="number"
              value={form.to_account}
              onChange={(e) =>
                setForm({ ...form, to_account: e.target.value })
              }
              required
            />

            <label>Amount</label>
            <input
              type="number"
              min="1"
              value={form.amount}
              onChange={(e) =>
                setForm({ ...form, amount: e.target.value })
              }
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

export default Transfer;