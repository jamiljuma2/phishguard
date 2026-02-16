import React, { useState } from 'react';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import Dashboard from './pages/Dashboard';
import History from './pages/History'; // New placeholder
import About from './pages/About'; // New placeholder
import Footer from './components/Footer';

function App() {
  const [currentPage, setCurrentPage] = useState('home');

  return (
    <div className="min-h-screen font-sans transition-colors duration-300 flex flex-col bg-gradient-to-br from-background-light via-white to-accent/10 dark:from-background-dark dark:via-slate-900 dark:to-accent/20">
      <Navbar currentPage={currentPage} setCurrentPage={setCurrentPage} />

      <main className="flex-grow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
          {currentPage === 'home' && <Home />}
          {currentPage === 'dashboard' && <Dashboard />}
          {currentPage === 'history' && <History />}
          {currentPage === 'about' && <About />}
        </div>
      </main>

      <Footer />
    </div>
  );
}

export default App;
