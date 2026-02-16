import React, { useState } from 'react';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import Dashboard from './pages/Dashboard';
import History from './pages/History'; // New placeholder
import About from './pages/About'; // New placeholder
import Footer from './components/Footer';
import Privacy from './pages/Privacy';
import Terms from './pages/Terms';
import Contact from './pages/Contact';

function App() {
  const [currentPage, setCurrentPage] = useState('home');

  // Simple client-side routing for footer links
  const [route, setRoute] = useState(window.location.pathname);
  React.useEffect(() => {
    const onPopState = () => setRoute(window.location.pathname);
    window.addEventListener('popstate', onPopState);
    return () => window.removeEventListener('popstate', onPopState);
  }, []);
  const navigate = (path) => {
    window.history.pushState({}, '', path);
    setRoute(path);
  };

  // Patch Footer links to use navigate
  React.useEffect(() => {
    const footer = document.querySelector('footer');
    if (footer) {
      footer.querySelectorAll('a').forEach(a => {
        if (a.pathname.startsWith('/privacy') || a.pathname.startsWith('/terms') || a.pathname.startsWith('/contact')) {
          a.onclick = (e) => {
            e.preventDefault();
            navigate(a.pathname);
          };
        }
      });
    }
  }, [route]);

  let PageComponent = null;
  if (route === '/privacy') PageComponent = <Privacy />;
  else if (route === '/terms') PageComponent = <Terms />;
  else if (route === '/contact') PageComponent = <Contact />;
  else PageComponent = (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
      {currentPage === 'home' && <Home />}
      {currentPage === 'dashboard' && <Dashboard />}
      {currentPage === 'history' && <History />}
      {currentPage === 'about' && <About />}
    </div>
  );

  return (
    <div className="min-h-screen font-sans transition-colors duration-300 flex flex-col bg-gradient-to-br from-background-light via-white to-accent/10 dark:from-background-dark dark:via-slate-900 dark:to-accent/20">
      <Navbar currentPage={currentPage} setCurrentPage={setCurrentPage} />
      <main className="flex-grow">{PageComponent}</main>
      <Footer />
    </div>
  );
}

export default App;
