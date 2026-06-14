import { useEffect, useState } from "react";
import api from "../../api/axios";
import DashboardLayout from "../../layouts/DashboardLayout";

function Beneficiaries() {
  const [beneficiaries, setBeneficiaries] = useState([]);

  const [form, setForm] = useState({
    nickname: "",
    beneficiary_name: "",
    beneficiary_account_no: "",
    beneficiary_ifsc: "",
  });

  useEffect(() => {
    loadBeneficiaries();
  }, []);

  async function loadBeneficiaries() {
    try {
      const res = await api.get("/beneficiaries/my-beneficiaries");
      setBeneficiaries(res.data);
    } catch (err) {
      console.error(err);
    }
  }

  async function addBeneficiary(e) {
    e.preventDefault();

    try {
      await api.post("/beneficiaries/add", {
        ...form,
        beneficiary_account_no: Number(form.beneficiary_account_no),
      });

      setForm({
        nickname: "",
        beneficiary_name: "",
        beneficiary_account_no: "",
        beneficiary_ifsc: "",
      });

      loadBeneficiaries();
    } catch (err) {
      console.error(err);
    }
  }

  async function deleteBeneficiary(id) {
    if (!window.confirm("Are you sure you want to delete this beneficiary?")) {
      return;
    }

    try {
      await api.delete(`/beneficiaries/${id}`);
      loadBeneficiaries();
    } catch (err) {
      console.error(err);
    }
  }

  return (
    <DashboardLayout>
      <h1>Manage Beneficiaries</h1>

      <form className="form-card" onSubmit={addBeneficiary}>
        <input
          placeholder="Nickname"
          value={form.nickname}
          onChange={(e) =>
            setForm({ ...form, nickname: e.target.value })
          }
        />

        <input
          placeholder="Beneficiary Name"
          value={form.beneficiary_name}
          onChange={(e) =>
            setForm({
              ...form,
              beneficiary_name: e.target.value,
            })
          }
        />

        <input
          type="number"
          placeholder="Account Number"
          value={form.beneficiary_account_no}
          onChange={(e) =>
            setForm({
              ...form,
              beneficiary_account_no: e.target.value,
            })
          }
        />

        <input
          placeholder="IFSC"
          value={form.beneficiary_ifsc}
          onChange={(e) =>
            setForm({
              ...form,
              beneficiary_ifsc: e.target.value,
            })
          }
        />

        <button type="submit">Add Beneficiary</button>
      </form>

      <table className="transaction-table">
        <thead>
          <tr>
            <th>Nickname</th>
            <th>Name</th>
            <th>Account</th>
            <th>IFSC</th>
            <th>Status</th>
            <th>Action</th>
          </tr>
        </thead>

        <tbody>
          {beneficiaries.map((b) => (
            <tr key={b.beneficiary_id}>
              <td>{b.nickname}</td>
              <td>{b.beneficiary_name}</td>
              <td>{b.beneficiary_account_no}</td>
              <td>{b.beneficiary_ifsc}</td>
              <td>{b.status}</td>
              <td>
                <button
                  onClick={() =>
                    deleteBeneficiary(b.beneficiary_id)
                  }
                >
                  Delete
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </DashboardLayout>
  );
}

export default Beneficiaries;