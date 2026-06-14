import Sidebar from "../components/Sidebar";
import Topbar from "../components/Topbar";
import Footer from "../components/Footer";

function DashboardLayout({ children }) {
  return (
    <div className="dashboard-layout">
      <Sidebar />

      <main className="main-area">
        <Topbar />

        <section className="dashboard-content">
          {children}
        </section>

        <Footer />
      </main>
    </div>
  );
}

export default DashboardLayout;