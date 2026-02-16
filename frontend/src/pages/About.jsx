import React from 'react';
import ReportModal from '../components/ReportModal';
import { Database, Cpu, ShieldCheck, Lock } from 'lucide-react';

function About() {
        const [modalOpen, setModalOpen] = React.useState(false);
        const sampleReport = {
            model: 'PhishGuard AI v2.0',
            dataset: '50,000+ emails',
            algorithms: ['Naive Bayes', 'TF-IDF', 'Heuristics'],
            privacy: 'GDPR Compliant, Encrypted',
        };
        return (
                <div className="max-w-4xl mx-auto space-y-12">
            <div className="text-center space-y-4">
                <h1 className="text-4xl font-display font-bold text-slate-900 dark:text-white">How PhishGuard AI Works</h1>
                <p className="text-xl text-slate-600 dark:text-slate-300 max-w-2xl mx-auto">
                    Our advanced machine learning model analyzes email patterns to detect threats that traditional filters miss.
                </p>
            </div>

            <div className="grid md:grid-cols-2 gap-8">
                <div className="card space-y-4">
                    <div className="w-12 h-12 rounded-lg bg-blue-100 dark:bg-blue-900/30 flex items-center justify-center text-blue-600 dark:text-blue-400">
                        <Database size={24} />
                    </div>
                    <h3 className="text-xl font-bold text-slate-900 dark:text-white">The Dataset</h3>
                    <p className="text-slate-600 dark:text-slate-400 leading-relaxed">
                        Trained on over 50,000 confirmed phishing emails and legitimate correspondence. Our dataset is continuously updated with the latest threat intelligence signatures.
                    </p>
                </div>

                <div className="card space-y-4">
                    <div className="w-12 h-12 rounded-lg bg-indigo-100 dark:bg-indigo-900/30 flex items-center justify-center text-indigo-600 dark:text-indigo-400">
                        <Cpu size={24} />
                    </div>
                    <h3 className="text-xl font-bold text-slate-900 dark:text-white">The Algorithm</h3>
                    <p className="text-slate-600 dark:text-slate-400 leading-relaxed">
                        Utilizes a hybrid approach combining Naive Bayes, TF-IDF Vectorization, and heuristic rule-based detection to identify suspicious URLs, urgency triggers, and spoofed domains.
                    </p>
                </div>
            </div>

            <div className="bg-slate-900 dark:bg-slate-800 rounded-3xl p-8 md:p-12 relative overflow-hidden shadow-2xl">
                <div className="absolute top-0 right-0 -mr-20 -mt-20 w-64 h-64 bg-accent/20 rounded-full blur-3xl"></div>
                <div className="absolute bottom-0 left-0 -ml-20 -mb-20 w-64 h-64 bg-highlight/20 rounded-full blur-3xl"></div>

                <div className="relative z-10 text-center space-y-6">
                    <ShieldCheck className="w-16 h-16 text-emerald-400 mx-auto" />
                    <h2 className="text-3xl font-display font-bold text-white">Enterprise-Grade Security</h2>
                    <p className="text-slate-300 max-w-2xl mx-auto">
                        Your data is processed locally in memory and never stored without your explicit permission. We adhere to the strictest data privacy standards.
                    </p>
                    <div className="flex justify-center gap-4 pt-4">
                        <div className="flex items-center gap-2 text-sm text-slate-400">
                            <Lock size={16} /> End-to-End Encrypted
                        </div>
                        <div className="flex items-center gap-2 text-sm text-slate-400">
                            <CheckCircle size={16} /> GDPR Compliant
                        </div>
                        <button className="btn-primary px-4 py-1 text-xs ml-4" onClick={() => setModalOpen(true)}>
                          View Sample Report
                        </button>
                    </div>
                    <ReportModal open={modalOpen} onClose={() => setModalOpen(false)} report={sampleReport} />
                </div>
            </div>
        </div>
    );
}

// Helper component since CheckCircle wasn't imported
function CheckCircle({ size }) {
    return (
        <svg
            xmlns="http://www.w3.org/2000/svg"
            width={size}
            height={size}
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
        >
            <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
            <polyline points="22 4 12 14.01 9 11.01"></polyline>
        </svg>
    );
}

export default About;
