import React, { useState } from 'react';
import ReportModal from '../components/ReportModal';
import EmailInput from '../components/EmailInput';
import ResultCard from '../components/ResultCard';
import api from '../api';
import { motion } from 'framer-motion';
import { Sparkles } from 'lucide-react';


function Home() {
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState(null);
    const [error, setError] = useState(null);
    const [modalOpen, setModalOpen] = useState(false);
    const [inputType, setInputType] = useState('email'); // 'email', 'sms', 'url'

    const analyzeInput = async (inputText) => {
        setLoading(true);
        setError(null);
        setResult(null);
        try {
            const response = await api.post('/predict', { text: inputText, type: inputType });
            setResult(response.data);
        } catch (err) {
            console.error(err);
            setError('Failed to analyze input. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="space-y-16">
            <div className="text-center space-y-6 max-w-3xl mx-auto">
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-accent/10 text-accent font-medium text-sm"
                >
                    <Sparkles size={16} />
                    <span>AI-Powered Threat Detection v2.0</span>
                </motion.div>

                <motion.h1
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.1 }}
                    className="text-5xl md:text-6xl font-display font-bold text-slate-900 dark:text-white leading-tight"
                >
                    Is that email <span className="text-transparent bg-clip-text bg-gradient-to-r from-accent to-highlight">safe?</span>
                </motion.h1>

                <motion.p
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.2 }}
                    className="text-xl text-slate-500 dark:text-slate-400"
                >
                    Paste any email content below. Our enterprise-grade AI scans for phishing patterns, malicious links, and social engineering tactics in milliseconds.
                </motion.p>
            </div>


            <div className="max-w-4xl mx-auto space-y-4">
                <div className="flex justify-center gap-4 mb-2">
                    <button
                        className={`px-4 py-2 rounded-lg font-medium border transition-colors ${inputType === 'email' ? 'bg-accent text-white' : 'bg-white dark:bg-slate-800 text-slate-700 dark:text-slate-200 border-accent'}`}
                        onClick={() => setInputType('email')}
                        type="button"
                    >
                        Email
                    </button>
                    <button
                        className={`px-4 py-2 rounded-lg font-medium border transition-colors ${inputType === 'sms' ? 'bg-accent text-white' : 'bg-white dark:bg-slate-800 text-slate-700 dark:text-slate-200 border-accent'}`}
                        onClick={() => setInputType('sms')}
                        type="button"
                    >
                        SMS
                    </button>
                    <button
                        className={`px-4 py-2 rounded-lg font-medium border transition-colors ${inputType === 'url' ? 'bg-accent text-white' : 'bg-white dark:bg-slate-800 text-slate-700 dark:text-slate-200 border-accent'}`}
                        onClick={() => setInputType('url')}
                        type="button"
                    >
                        URL
                    </button>
                </div>
                <EmailInput onAnalyze={analyzeInput} loading={loading} inputType={inputType} />
            </div>

            {error && (
                <div className="max-w-3xl mx-auto p-4 bg-red-50 border-l-4 border-red-500 text-red-700 rounded-r-lg shadow-sm">
                    <p>{error}</p>
                </div>
            )}

                        {result && (
                                <>
                                    <div className="max-w-4xl mx-auto pb-10">
                                        <ResultCard result={result} />
                                        <div className="flex justify-end mt-4">
                                            <button className="btn-primary px-6 py-2 text-sm" onClick={() => setModalOpen(true)}>
                                                View Full Report
                                            </button>
                                        </div>
                                    </div>
                                    <ReportModal open={modalOpen} onClose={() => setModalOpen(false)} report={result} />
                                </>
                        )}
        </div>
    );
}

export default Home;
