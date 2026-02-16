import React from 'react';
import { motion } from 'framer-motion';
import { ShieldAlert, ShieldCheck, AlertTriangle, Eye } from 'lucide-react';
import PropTypes from 'prop-types';

function ResultCard({ result }) {
    const isPhishing = result.result === 'Phishing';
    const confidencePercent = (result.confidence * 100).toFixed(1);
    const color = isPhishing ? 'red' : 'emerald';
    const textColor = isPhishing ? 'text-red-500' : 'text-emerald-500';
    const borderColor = isPhishing ? 'border-red-500' : 'border-emerald-500';
    const bgColor = isPhishing ? 'bg-red-50 dark:bg-red-900/10' : 'bg-emerald-50 dark:bg-emerald-900/10';
    const inputTypeLabel = result.input_type ? result.input_type.charAt(0).toUpperCase() + result.input_type.slice(1) : 'Input';

    return (
        <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.5, type: "spring" }}
            className={`rounded-2xl shadow-xl overflow-hidden bg-white dark:bg-slate-800 border-l-8 ${borderColor}`}
        >
            <div className="p-8">
                <div className="flex flex-col md:flex-row items-center justify-between gap-6">
                    <div className="flex items-center gap-6">
                        <motion.div
                            initial={{ rotate: -180, opacity: 0 }}
                            animate={{ rotate: 0, opacity: 1 }}
                            transition={{ duration: 0.8, delay: 0.2 }}
                            className={`p-4 rounded-full ${bgColor}`}
                        >
                            {isPhishing ? (
                                <ShieldAlert className="w-12 h-12 text-red-500" />
                            ) : (
                                <ShieldCheck className="w-12 h-12 text-emerald-500" />
                            )}
                        </motion.div>

                        <div>
                            <h3 className={`text-3xl font-display font-bold ${textColor}`}>
                                {isPhishing
                                    ? `Phishing Detected (${inputTypeLabel})`
                                    : `Legitimate ${inputTypeLabel}`}
                            </h3>
                            <p className="mt-2 text-slate-500 dark:text-slate-400 flex items-center gap-2">
                                {isPhishing
                                    ? 'High risk. Do not click links or download attachments.'
                                    : 'Safe interactions detected. Standard caution advised.'}
                            </p>
                        </div>
                    </div>

                    <div className="text-right min-w-[150px]">
                        <span className="text-sm font-medium text-slate-500 dark:text-slate-400 uppercase tracking-wider">Confidence Score</span>
                        <div className="flex items-end justify-end gap-1 mt-1">
                            <span className={`text-4xl font-mono font-bold ${textColor}`}>{confidencePercent}%</span>
                        </div>
                        {/* Progress Bar */}
                        <div className="w-full bg-slate-200 dark:bg-slate-700 rounded-full h-2 mt-3 overflow-hidden">
                            <motion.div
                                initial={{ width: 0 }}
                                animate={{ width: `${confidencePercent}%` }}
                                transition={{ duration: 1, delay: 0.5 }}
                                className={`h-full rounded-full ${isPhishing ? 'bg-red-500' : 'bg-emerald-500'}`}
                            />
                        </div>
                    </div>
                </div>

                {/* Detailed Breakdown */}
                <div className="mt-10 grid md:grid-cols-2 gap-6">

                    {/* Heuristics Panel */}
                    <div className="bg-slate-50 dark:bg-slate-900/50 rounded-xl p-5 border border-slate-100 dark:border-slate-700">
                        <h4 className="flex items-center gap-2 font-semibold text-slate-900 dark:text-white mb-4">
                            <Eye size={18} className="text-accent" />
                            Analysis Summary
                        </h4>
                        <ul className="space-y-3">
                            <li className="flex justify-between text-sm">
                                <span className="text-slate-600 dark:text-slate-400">Suspicious Keywords</span>
                                <span className="font-mono font-medium text-slate-900 dark:text-white">{result.heuristics?.suspicious_keyword_count || 0}</span>
                            </li>
                            <li className="flex justify-between text-sm">
                                <span className="text-slate-600 dark:text-slate-400">URLs Detected</span>
                                <span className="font-mono font-medium text-slate-900 dark:text-white">{result.heuristics?.url_count || 0}</span>
                            </li>
                        </ul>
                    </div>

                    {/* Evidence Panel */}
                    <div className="bg-slate-50 dark:bg-slate-900/50 rounded-xl p-5 border border-slate-100 dark:border-slate-700">
                        <h4 className="flex items-center gap-2 font-semibold text-slate-900 dark:text-white mb-4">
                            <AlertTriangle size={18} className="text-warning" />
                            Evidence
                        </h4>
                        {result.suspicious_words && result.suspicious_words.length > 0 ? (
                            <div className="flex flex-wrap gap-2">
                                {result.suspicious_words.map((word, idx) => (
                                    <span key={idx} className="inline-flex items-center px-2.5 py-1 rounded-md text-xs font-medium bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-400">
                                        {word}
                                    </span>
                                ))}
                            </div>
                        ) : (
                            <p className="text-sm text-slate-500 italic">No specific suspicious terms flagged.</p>
                        )}
                    </div>
                </div>
            </div>

            {/* Footer Disclaimer */}
            <div className="bg-slate-50 dark:bg-slate-900/80 px-8 py-4 border-t border-slate-100 dark:border-slate-800">
                <p className="text-xs text-slate-400 dark:text-slate-500 text-center">
                    AI analysis is probabilistic. Always verify the sender manually before taking action.
                </p>
            </div>
        </motion.div>
    );
}

ResultCard.propTypes = {
    result: PropTypes.shape({
        result: PropTypes.string,
        confidence: PropTypes.number,
        heuristics: PropTypes.shape({
            suspicious_keyword_count: PropTypes.number,
            url_count: PropTypes.number,
        }),
        suspicious_words: PropTypes.arrayOf(PropTypes.string),
    }),
};

ResultCard.defaultProps = {
    result: {
        result: 'Unknown',
        confidence: 0,
        heuristics: {},
        suspicious_words: [],
    }
};

export default ResultCard;
