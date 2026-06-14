import { BrowserRouter, Routes, Route } from "react-router-dom";
import Login from "./pages/Login/Login";
import Dashboard from "./pages/Dashboard/Dashboard";
import ProtectedRoute from "./components/ProtectedRoute";
import Accounts from "./pages/Accounts/Accounts";
import Deposit from "./pages/Deposit/Deposit";
import Withdraw from "./pages/Withdraw/Withdraw";
import Transfer from "./pages/Transfer/Transfer";
import Transactions from "./pages/Transactions/Transactions";
import Beneficiaries from "./pages/Beneficiaries/Beneficiaries";
import Register from "./pages/Register/Register";
import NotFound from "./pages/NotFound/NotFound";
import Loans from "./pages/Loans/Loans";
function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/"                 element={<Login                                                  />}/>
        <Route path="/dashboard"        element={<ProtectedRoute><Dashboard             /></ProtectedRoute>}/>
        <Route path="/accounts"         element={<ProtectedRoute><Accounts              /></ProtectedRoute>}/>
        <Route path="/deposit"          element={<ProtectedRoute><Deposit               /></ProtectedRoute>}/>
        <Route path="/withdraw"         element={<ProtectedRoute><Withdraw              /></ProtectedRoute>}/>
        <Route path="/transfer"         element={<ProtectedRoute><Transfer              /></ProtectedRoute>}/>
        <Route path="/transactions"     element={<ProtectedRoute><Transactions          /></ProtectedRoute>}/>
        <Route path="/beneficiaries"    element={<ProtectedRoute><Beneficiaries         /></ProtectedRoute>}/>
        <Route path="/loans"            element={<ProtectedRoute><Loans                 /></ProtectedRoute>}/>
        <Route path="/register"         element={<Register                                               />}/>
        <Route path="*"                 element={<NotFound                                               />}/>
      </Routes>
    </BrowserRouter>
  );
}

export default App;