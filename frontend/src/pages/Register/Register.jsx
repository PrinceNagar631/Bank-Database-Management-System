import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../../api/axios";
import "./Register.css";

function Register() {
  const navigate = useNavigate();

  const [form, setForm] = useState({
    username: "",
    password: "",
    pin: "",
    email: "",
    phone_no: "",
    aadhaar: "",
    pan: "",
    first_name: "",
    last_name: "",
    gender: "",
    dob: "",
  });

  const [message, setMessage] = useState("");
  const [submitting, setSubmitting] = useState(false);

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);

    try {
      await api.post("/customers/register-individual", form);

      setMessage("Registration successful. Please login.");

      setTimeout(() => {
        navigate("/");
      }, 1500);
    } catch (err) {
      setMessage(
        typeof err.response?.data?.detail === "string"
          ? err.response.data.detail
          : "Registration failed. Please try again."
      );
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="register-container">
      <form className="register-card" onSubmit={handleSubmit}>
        <h1>Create Account</h1>

        {message && <div className="message">{message}</div>}

        <input name="username" placeholder="Username" onChange={handleChange} required />
        <input name="password" type="password" placeholder="Password" onChange={handleChange} required />
        <input name="pin" placeholder="4 Digit PIN" onChange={handleChange} required />
        <input name="first_name" placeholder="First Name" onChange={handleChange} required />
        <input name="last_name" placeholder="Last Name" onChange={handleChange} required />
        <input name="email" type="email" placeholder="Email" onChange={handleChange} required />
        <input name="phone_no" placeholder="Phone Number" onChange={handleChange} required />
        <input name="aadhaar" placeholder="Aadhaar Number" onChange={handleChange} required />
        <input name="pan" placeholder="PAN Number" onChange={handleChange} required />

        <select name="gender" onChange={handleChange} required>
          <option value="">Select Gender</option>
          <option>Male</option>
          <option>Female</option>
          <option>Other</option>
        </select>

        <input name="dob" type="date" onChange={handleChange} required />

        <button type="submit" disabled={submitting}>
          {submitting ? "Processing..." : "Submit"}
        </button>
      </form>
    </div>
  );
}

export default Register;