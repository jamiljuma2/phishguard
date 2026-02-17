import React, { useState, useCallback } from "react";
import Navbar from "./components/Navbar";
import Home from "./pages/Home";
import Dashboard from "./pages/Dashboard";
import History from "./pages/History";
import About from "./pages/About";
import Footer from "./components/Footer";
import Privacy from "./pages/Privacy";
import Terms from "./pages/Terms";
import Contact from "./pages/Contact";

function App() {
  const [currentPage, setCurrentPage] = useState("home");

  // Unified navigation: supports both main pages and footer pages
  const [route, setRoute] = useState(window.location.pathname);
  React.useEffect(() => {
    const onPopState = (e) => {
      const path = window.location.pathname;
      setRoute(path);
      if (path === "/" || path === "") {
        setCurrentPage(e.state?.page || "home");
      }
    };
    window.addEventListener("popstate", onPopState);
    return () => window.removeEventListener("popstate", onPopState);
  }, []);

  const navigate = useCallback((path) => {
    window.history.pushState({}, "", path);
    setRoute(path);
  }, []);

  // When navbar changes page, also update the route
  const handleSetCurrentPage = useCallback((page) => {
    setCurrentPage(page);
    setRoute("/");
    window.history.pushState({ page }, "", "/");
  }, []);

  let PageComponent = null;
  if (route === "/privacy") PageComponent = <Privacy />;
  else if (route === "/terms") PageComponent = <Terms />;
  else if (route === "/contact") PageComponent = <Contact />;
  else
    PageComponent = (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
        {currentPage === "home" && <Home />}
        {currentPage === "dashboard" && <Dashboard />}
        {currentPage === "history" && <History />}
        {currentPage === "about" && <About />}
      </div>
    );

  return (
    <div className="min-h-screen font-sans transition-colors duration-300 flex flex-col bg-gradient-to-br from-background-light via-white to-accent/10 dark:from-background-dark dark:via-slate-900 dark:to-accent/20">
      <Navbar currentPage={currentPage} setCurrentPage={handleSetCurrentPage} />
      <main className="flex-grow">{PageComponent}</main>
      <Footer navigate={navigate} />
    </div>
  );
}

export default App;
