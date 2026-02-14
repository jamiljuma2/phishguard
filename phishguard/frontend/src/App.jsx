import React, { useState } from 'react';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import Dashboard from './pages/Dashboard';
import History from './pages/History'; // New placeholder
import About from './pages/About'; // New placeholder

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

      <footer className="bg-white/90 dark:bg-slate-900/90 border-t border-slate-200 dark:border-slate-800 mt-auto transition-colors duration-300 shadow-inner">
        <div className="max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <p className="text-slate-500 dark:text-slate-400 text-sm mb-4 md:mb-0">
              © 2026 PhishGuard AI. Protecting clarity in a chaotic web.
            </p>
            <div className="flex space-x-6">
              <a href="#" className="text-slate-400 hover:text-accent transition-colors">Privacy</a>
              <a href="#" className="text-slate-400 hover:text-accent transition-colors">Terms</a>
              <a href="#" className="text-slate-400 hover:text-accent transition-colors">Contact</a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;
