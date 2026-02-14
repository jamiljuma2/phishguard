import React, { useState } from 'react';
import { Send, FileText } from 'lucide-react';
import { motion } from 'framer-motion';
import PropTypes from 'prop-types';

function EmailInput({ onAnalyze, loading }) {
    const [text, setText] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        if (text.trim()) {
            onAnalyze(text);
        }
    };

    const handlePasteExample = () => {
        setText("URGENT: Your account has been suspended! Click here to verify your identity immediately: http://paypal-secure-login.xyz");
    };

    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="w-full"
        >
            <form onSubmit={handleSubmit} className="space-y-6">
                <div className="relative group">
                    <div className="absolute -inset-0.5 bg-gradient-to-r from-accent to-highlight opacity-30 group-hover:opacity-100 transition duration-500 rounded-xl blur"></div>
                    <div className="relative bg-white dark:bg-slate-900 rounded-xl p-1">
                        <div className="flex justify-between items-center px-4 py-2 border-b border-slate-100 dark:border-slate-800">
                            <div className="flex items-center gap-2 text-slate-400 text-sm">
                                <FileText size={16} />
                                <span className="font-medium">New Scan</span>
                            </div>
                            <button
                                type="button"
                                onClick={handlePasteExample}
                                className="text-xs text-accent hover:text-accent-light font-medium transition-colors"
                            >
                                Paste Example Phishing Email
                            </button>
                        </div>

                        <textarea
                            id="email-content"
                            rows={10}
                            className="block w-full border-0 bg-transparent p-4 text-slate-900 dark:text-slate-100 placeholder:text-slate-400 focus:ring-0 sm:text-sm font-mono resize-none leading-relaxed"
                            placeholder="Paste the suspicious email header and body here..."
                            value={text}
                            onChange={(e) => setText(e.target.value)}
                            required
                        />
                    </div>
                </div>

                <div className="flex justify-center">
                    <button
                        type="submit"
                        disabled={loading || !text.trim()}
                        className={`
              relative overflow-hidden group btn-primary text-lg px-10 py-4 rounded-xl
              ${loading ? 'opacity-80 cursor-wait' : ''}
            `}
                    >
                        <span className="relative z-10 flex items-center gap-3">
                            {loading ? (
                                <>
                                    <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                    </svg>
                                    Analyzing Patterns...
                                </>
                            ) : (
                                <>
                                    <Send className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
                                    Analyze Email
                                </>
                            )}
                        </span>
                        {loading && (
                            <motion.div
                                className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent"
                                animate={{ x: ['-100%', '200%'] }}
                                transition={{ repeat: Infinity, duration: 1.5, ease: "linear" }}
                            />
                        )}
                    </button>
                </div>
            </form>
        </motion.div>
    );
}

EmailInput.propTypes = {
    onAnalyze: PropTypes.func.isRequired,
    loading: PropTypes.bool.isRequired,
};

export default EmailInput;
