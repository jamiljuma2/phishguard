import React from 'react';
import { X } from 'lucide-react';
import PropTypes from 'prop-types';

function ReportModal({ open, onClose, report }) {
  if (!open) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 backdrop-blur-sm">
      <div className="bg-white dark:bg-slate-900 rounded-2xl shadow-2xl max-w-2xl w-full p-8 relative">
        <button
          className="absolute top-4 right-4 text-slate-400 hover:text-accent transition-colors"
          onClick={onClose}
          aria-label="Close report"
        >
          <X size={24} />
        </button>
        <h2 className="text-2xl font-bold mb-4 text-slate-900 dark:text-white">Scan Report</h2>
        {report ? (
          <pre className="bg-slate-50 dark:bg-slate-800 rounded-lg p-4 text-sm text-slate-700 dark:text-slate-200 overflow-x-auto">
            {JSON.stringify(report, null, 2)}
          </pre>
        ) : (
          <p className="text-slate-500 dark:text-slate-400">No report data available.</p>
        )}
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
