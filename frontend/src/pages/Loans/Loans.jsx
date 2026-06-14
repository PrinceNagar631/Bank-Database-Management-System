import { useEffect, useState } from "react";
import api from "../../api/axios";
import DashboardLayout from "../../layouts/DashboardLayout";
import "../Transfer/Transfer.css";
import "../Transactions/Transactions.css";
function Loans() {
  const [loans, setLoans] = useState([]);
  const [message, setMessage] = useState("");

  const [form, setForm] = useState({
    branch_id: "",
    loan_type: "",
    principal_amount: "",
    interest_rate: "",
    loan_term_months: "",
  });

  useEffect(() => {
    loadLoans();
  }, []);

  async function loadLoans() {
    try {
      const res = await api.get("/loan/my-loans");
      setLoans(res.data);
    } catch (err) {
      console.error(err);
    }
  }

  async function applyLoan(e) {
    e.preventDefault();

    try {
      await api.post("/loan/apply", {
        branch_id: Number(form.branch_id),
        loan_type: form.loan_type,
        principal_amount: Number(form.principal_amount),
        interest_rate: Number(form.interest_rate),
        loan_term_months: Number(form.loan_term_months),
      });

      setMessage("Loan application submitted successfully.");

      setForm({
        branch_id: "",
        loan_type: "",
        principal_amount: "",
        interest_rate: "",
        loan_term_months: "",
      });

      loadLoans();
    } catch (err) {
      setMessage("Failed to apply for loan.");
    }
  }

  return (
    <DashboardLayout>
      <h1>Loans</h1>

      {message && <div className="success-message">{message}</div>}

      <div className="form-card">
        <h2>Apply for Loan</h2>

        <form onSubmit={applyLoan}>
          <input
            type="number"
            placeholder="Branch ID"
            value={form.branch_id}
            onChange={(e) =>
              setForm({ ...form, branch_id: e.target.value })
            }
            required
          />

          <input
            type="text"
            placeholder="Loan Type"
            value={form.loan_type}
            onChange={(e) =>
              setForm({ ...form, loan_type: e.target.value })
            }
            required
          />

          <input
            type="number"
            placeholder="Principal Amount"
            value={form.principal_amount}
            onChange={(e) =>
              setForm({
                ...form,
                principal_amount: e.target.value,
              })
            }
            required
          />

          <input
            type="number"
            step="0.01"
            placeholder="Interest Rate"
            value={form.interest_rate}
            onChange={(e) =>
              setForm({
                ...form,
                interest_rate: e.target.value,
              })
            }
            required
          />

          <input
            type="number"
            placeholder="Loan Term (Months)"
            value={form.loan_term_months}
            onChange={(e) =>
              setForm({
                ...form,
                loan_term_months: e.target.value,
              })
            }
            required
          />

          <button type="submit">Apply</button>
        </form>
      </div>

      <h2 style={{ marginTop: "30px" }}>My Loans</h2>

      <table className="transaction-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Type</th>
            <th>Principal</th>
            <th>Interest</th>
            <th>Term</th>
            <th>Status</th>
          </tr>
        </thead>

        <tbody>
          {loans.map((loan) => (
            <tr key={loan.loan_id}>
              <td>{loan.loan_id}</td>
              <td>{loan.loan_type}</td>
              <td>₹ {loan.principal_amount}</td>
              <td>{loan.interest_rate}%</td>
              <td>{loan.loan_term_months}</td>
              <td>{loan.status}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </DashboardLayout>
  );
}

export default Loans;