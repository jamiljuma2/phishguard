import React from "react";
import PropTypes from "prop-types";

function Footer({ navigate }) {
  const handleClick = (e, path) => {
    e.preventDefault();
    if (navigate) navigate(path);
  };

  return (
    <footer className="w-full py-6 mt-16 border-t border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 text-center text-sm text-slate-500 dark:text-slate-400">
      <div className="container mx-auto flex flex-col md:flex-row justify-center items-center gap-4">
        <span>
          &copy; {new Date().getFullYear()} PhishGuard. All rights reserved.
        </span>
        <div className="flex gap-4">
          <a
            href="/privacy"
            onClick={(e) => handleClick(e, "/privacy")}
            className="hover:text-accent underline transition-colors"
          >
            Privacy Policy
          </a>
          <a
            href="/terms"
            onClick={(e) => handleClick(e, "/terms")}
            className="hover:text-accent underline transition-colors"
          >
            Terms of Service
          </a>
          <a
            href="/contact"
            onClick={(e) => handleClick(e, "/contact")}
            className="hover:text-accent underline transition-colors"
          >
            Contact
          </a>
        </div>
      </div>
    </footer>
  );
}

Footer.propTypes = {
  navigate: PropTypes.func,
};

export default Footer;
