import React from 'react';
import { X } from 'lucide-react';
import PropTypes from 'prop-types';


function ReportModal({ open, onClose, report }) {
  if (!open) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 backdrop-blur-sm">
      <div className="bg-white dark:bg-slate-900 rounded-2xl shadow-2xl w-full max-w-3xl max-h-[90vh] flex flex-col relative overflow-hidden">
        {/* Close Tab/Bar */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-slate-100 dark:border-slate-800 bg-slate-50 dark:bg-slate-800 sticky top-0 z-10">
          <h2 className="text-2xl font-bold text-slate-900 dark:text-white">Scan Report</h2>
          <button
            className="rounded-full p-2 text-slate-400 hover:text-accent hover:bg-slate-100 dark:hover:bg-slate-700 transition-colors"
            onClick={onClose}
            aria-label="Close report"
          >
            <X size={28} />
          </button>
        </div>
        <div className="flex-1 overflow-auto px-6 py-4">
          {report ? (
            <div className="space-y-4">
              {/* Key fields summary */}
              <div className="grid md:grid-cols-2 gap-6">
                <div className="bg-slate-50 dark:bg-slate-800 rounded-xl p-4 border border-slate-100 dark:border-slate-700">
                  <h3 className="font-semibold text-slate-900 dark:text-white mb-2">Summary</h3>
                  <ul className="text-sm text-slate-700 dark:text-slate-200 space-y-1">
                    <li><span className="font-medium">Type:</span> {report.input_type || report.type || 'N/A'}</li>
                    <li><span className="font-medium">Result:</span> {report.result}</li>
                    <li><span className="font-medium">Confidence:</span> {typeof report.confidence === 'number' ? (report.confidence * 100).toFixed(1) + '%' : 'N/A'}</li>
                    {report.subject && <li><span className="font-medium">Subject:</span> {report.subject}</li>}
                    {report.email && <li><span className="font-medium">Email:</span> {report.email}</li>}
                  </ul>
                </div>
                <div className="bg-slate-50 dark:bg-slate-800 rounded-xl p-4 border border-slate-100 dark:border-slate-700">
                  <h3 className="font-semibold text-slate-900 dark:text-white mb-2">Input</h3>
                  <div className="text-xs bg-slate-100 dark:bg-slate-900 rounded p-2 font-mono break-words whitespace-pre-wrap max-h-40 overflow-auto">
                    {report.input || report.email_text || report.email || report.subject || 'N/A'}
                  </div>
                </div>
              </div>
              {/* Heuristics */}
              {report.heuristics && (
                <div className="bg-slate-50 dark:bg-slate-800 rounded-xl p-4 border border-slate-100 dark:border-slate-700">
                  <h3 className="font-semibold text-slate-900 dark:text-white mb-2">Heuristics</h3>
                  <ul className="text-sm text-slate-700 dark:text-slate-200 space-y-1">
                    {Object.entries(report.heuristics).map(([k, v]) => (
                      <li key={k}><span className="font-medium">{k.replace(/_/g, ' ')}:</span> {v}</li>
                    ))}
                  </ul>
                </div>
              )}
              {/* Suspicious Words */}
              {report.suspicious_words && report.suspicious_words.length > 0 && (
                <div className="bg-slate-50 dark:bg-slate-800 rounded-xl p-4 border border-slate-100 dark:border-slate-700">
                  <h3 className="font-semibold text-slate-900 dark:text-white mb-2">Suspicious Words</h3>
                  <div className="flex flex-wrap gap-2">
                    {report.suspicious_words.map((word, idx) => (
                      <span key={idx} className="inline-flex items-center px-2.5 py-1 rounded-md text-xs font-medium bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-400">{word}</span>
                    ))}
                  </div>
                </div>
              )}
              {/* Raw JSON */}
              <div className="bg-slate-100 dark:bg-slate-900 rounded-xl p-4 border border-slate-200 dark:border-slate-800">
                <h3 className="font-semibold text-slate-900 dark:text-white mb-2">Full JSON</h3>
                <pre className="text-xs text-slate-700 dark:text-slate-200 overflow-x-auto whitespace-pre-wrap break-words max-h-60">{JSON.stringify(report, null, 2)}</pre>
              </div>
            </div>
          ) : (
            <p className="text-slate-500 dark:text-slate-400">No report data available.</p>
          )}
        </div>
      </div>
    </div>
  );
}

ReportModal.propTypes = {
  open: PropTypes.bool.isRequired,
  onClose: PropTypes.func.isRequired,
  report: PropTypes.object,
};

export default ReportModal;
