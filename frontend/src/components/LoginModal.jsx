import { useEffect } from "react";
import Auth from "./Auth";
import PropTypes from "prop-types";

const LoginModal = ({ isOpen, onClose }) => {
  useEffect(() => {
    if (!isOpen) return;
    const handleEscape = (e) => {
      if (e.key === "Escape") onClose();
    };
    document.addEventListener("keydown", handleEscape);
    return () => document.removeEventListener("keydown", handleEscape);
  }, [isOpen, onClose]);

  if (!isOpen) {
    return null;
  }

  return (
    <div
      className="fixed inset-0 bg-black bg-opacity-60 z-50 flex justify-center items-center"
      onClick={onClose}
      role="dialog"
      aria-modal="true"
      aria-label="Sign in to PhishGuard"
    >
      <div
        className="bg-white dark:bg-slate-800 p-8 rounded-xl shadow-2xl w-full max-w-sm text-center transform transition-all"
        onClick={(e) => e.stopPropagation()}
      >
        <h2 className="text-2xl font-bold text-slate-900 dark:text-white mb-2">
          Welcome to PhishGuard
        </h2>
        <p className="text-slate-600 dark:text-slate-400 mb-6">
          Sign in to save and view your scan history.
        </p>
        <div className="space-y-4">
          <Auth onSuccess={onClose} />
          <p className="text-xs text-slate-500">
            By continuing, you agree to our Terms of Service and Privacy Policy.
          </p>
        </div>
        <button
          onClick={onClose}
          className="mt-6 text-sm text-slate-500 hover:text-slate-700 dark:hover:text-slate-300 transition-colors"
        >
          Maybe later
        </button>
      </div>
    </div>
  );
};

LoginModal.propTypes = {
  isOpen: PropTypes.bool.isRequired,
  onClose: PropTypes.func.isRequired,
};

export default LoginModal;
