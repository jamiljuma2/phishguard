import React, { useState, useEffect } from 'react';
import { Shield, Menu, X, Sun, Moon } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import PropTypes from 'prop-types';

function Navbar({ currentPage, setCurrentPage }) {
    const [isOpen, setIsOpen] = useState(false);
    const [isDark, setIsDark] = useState(false);

    // Toggle Dark Mode
    useEffect(() => {
        if (isDark) {
            document.documentElement.classList.add('dark');
        } else {
            document.documentElement.classList.remove('dark');
        }
    }, [isDark]);

    const toggleTheme = () => setIsDark(!isDark);

    const navLinks = [
        { id: 'home', label: 'Analyzer' },
        { id: 'dashboard', label: 'Dashboard' },
        { id: 'history', label: 'Scan History' },
        { id: 'about', label: 'About Model' },
    ];

    return (
        <nav className="sticky top-0 z-50 bg-white/80 dark:bg-slate-900/80 backdrop-blur-md border-b border-slate-200 dark:border-slate-800 transition-colors duration-300">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex justify-between h-20 items-center">
                    {/* Logo */}
                    <div className="flex-shrink-0 flex items-center gap-3 cursor-pointer" onClick={() => setCurrentPage('home')}>
                        <div className="bg-gradient-to-br from-highlight to-accent p-2 rounded-lg shadow-lg">
                            <Shield className="h-6 w-6 text-white" />
                        </div>
                        <span className="text-2xl font-display font-bold text-slate-900 dark:text-white tracking-tight">
                            PhishGuard
                        </span>
                    </div>

                    {/* Desktop Nav */}
                    <div className="hidden md:flex items-center space-x-8">
                        {navLinks.map((link) => (
                            <button
                                key={link.id}
                                onClick={() => setCurrentPage(link.id)}
                                className={`text-sm font-medium transition-colors duration-200 ${currentPage === link.id
                                    ? 'text-accent dark:text-accent-light'
                                    : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white'
                                    }`}
                            >
                                {link.label}
                            </button>
                        ))}

                        {/* Theme Toggle */}
                        <button
                            onClick={toggleTheme}
                            className="p-2 rounded-full bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 hover:text-accent dark:hover:text-accent-light transition-colors"
                        >
                            {isDark ? <Sun size={20} /> : <Moon size={20} />}
                        </button>

                        {/* Profile Avatar (Mock) */}
                        <div className="h-8 w-8 rounded-full bg-gradient-to-r from-teal-400 to-blue-500 ring-2 ring-white dark:ring-slate-800 shadow-sm" />
                    </div>

                    {/* Mobile Menu Button */}
                    <div className="md:hidden flex items-center gap-4">
                        <button
                            onClick={toggleTheme}
                            className="p-2 rounded-full bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400"
                        >
                            {isDark ? <Sun size={20} /> : <Moon size={20} />}
                        </button>
                        <button
                            onClick={() => setIsOpen(!isOpen)}
                            className="text-slate-600 dark:text-slate-300 hover:text-slate-900 dark:hover:text-white"
                        >
                            {isOpen ? <X size={28} /> : <Menu size={28} />}
                        </button>
                    </div>
                </div>
            </div>

            {/* Mobile Menu */}
            <AnimatePresence>
                {isOpen && (
                    <motion.div
                        initial={{ opacity: 0, height: 0 }}
                        animate={{ opacity: 1, height: 'auto' }}
                        exit={{ opacity: 0, height: 0 }}
                        className="md:hidden bg-white dark:bg-slate-900 border-b border-slate-200 dark:border-slate-800"
                    >
                        <div className="px-4 pt-2 pb-6 space-y-2">
                            {navLinks.map((link) => (
                                <button
                                    key={link.id}
                                    onClick={() => {
                                        setCurrentPage(link.id);
                                        setIsOpen(false);
                                    }}
                                    className={`block w-full text-left px-3 py-4 text-base font-medium rounded-md ${currentPage === link.id
                                        ? 'bg-indigo-50 dark:bg-indigo-900/20 text-accent dark:text-accent-light'
                                        : 'text-slate-600 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800'
                                        }`}
                                >
                                    {link.label}
                                </button>
                            ))}
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>
        </nav>
    );
}

Navbar.propTypes = {
    currentPage: PropTypes.string.isRequired,
    setCurrentPage: PropTypes.func.isRequired,
};

export default Navbar;
