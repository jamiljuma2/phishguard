import React, { useState } from "react";
import { auth } from "../firebase";
import {
    GoogleAuthProvider,
    signInWithPopup,
    createUserWithEmailAndPassword,
    signInWithEmailAndPassword,
} from "firebase/auth";

const Auth = () => {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState(null);

    const googleSignIn = async () => {
        const provider = new GoogleAuthProvider();
        try {
            await signInWithPopup(auth, provider);
        } catch (error) {
            console.error(error);
            setError(error.message);
        }
    };

    const emailSignUp = async () => {
        try {
            await createUserWithEmailAndPassword(auth, email, password);
        } catch (error) {
            console.error(error);
            setError(error.message);
        }
    };

    const emailSignIn = async () => {
        try {
            await signInWithEmailAndPassword(auth, email, password);
        } catch (error) {
            console.error(error);
            setError(error.message);
        }
    };

    return (
        <div className="space-y-4">
            {error && <p className="text-red-500 text-sm">{error}</p>}
            <input
                type="email"
                placeholder="Email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full px-4 py-2 border border-slate-300 dark:border-slate-600 rounded-lg bg-white dark:bg-slate-700 text-slate-900 dark:text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-accent-light"
            />
            <input
                type="password"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full px-4 py-2 border border-slate-300 dark:border-slate-600 rounded-lg bg-white dark:bg-slate-700 text-slate-900 dark:text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-accent-light"
            />
            <button
                onClick={emailSignIn}
                className="w-full px-4 py-2 bg-accent dark:bg-accent-light text-white rounded-lg hover:bg-accent-dark dark:hover:bg-accent transition-colors duration-300"
            >
                Sign In with Email
            </button>
            <button
                onClick={emailSignUp}
                className="w-full px-4 py-2 bg-highlight dark:bg-highlight-light text-white rounded-lg hover:bg-highlight-dark dark:hover:bg-highlight transition-colors duration-300"
            >
                Sign Up with Email
            </button>
            <div className="relative flex items-center justify-center">
                <div className="absolute inset-x-0 top-1/2 h-px -translate-y-1/2 bg-slate-200 dark:bg-slate-700"></div>
                <div className="relative bg-white dark:bg-slate-800 px-4 text-sm font-medium text-slate-500 dark:text-slate-400">
                    Or
                </div>
            </div>
            <button
                onClick={googleSignIn}
                className="w-full flex items-center justify-center gap-2 px-4 py-2 bg-white border border-slate-200 dark:border-slate-700 rounded-lg text-slate-700 dark:text-slate-200 hover:bg-slate-50 dark:hover:bg-slate-700 transition-colors duration-300"
            >
                <svg
                    version="1.1"
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 48 48"
                    className="w-5 h-5"
                >
                    <path
                        fill="#4285F4"
                        d="M43.611 20.083H42V20H24v8h11.303c-1.649 4.657-6.08 8-11.303 8c-6.627 0-12-5.373-12-12s5.373-12 12-12c3.059 0 5.842 1.154 7.961 3.039l5.657-5.657C34.046 6.053 29.268 4 24 4C12.955 4 4 12.955 4 24s8.955 20 20 20s20-8.955 20-20c0-1.341-.138-2.65-.389-3.917z"
                    />
                    <path
                        fill="#34A853"
                        d="m6.306 14.691l6.571 4.819C14.655 15.108 18.961 12 24 12c3.059 0 5.842 1.154 7.961 3.039l5.657-5.657C34.046 6.053 29.268 4 24 4C16.318 4 9.656 8.337 6.306 14.691z"
                    />
                    <path
                        fill="#FBBC05"
                        d="M24 44c5.166 0 9.86-1.977 13.409-5.192l-6.19-5.238C29.211 35.091 26.715 36 24 36c-5.202 0-9.619-3.317-11.283-7.946l-6.522 5.025C9.505 39.556 16.227 44 24 44z"
                    />
                    <path
                        fill="#EA4335"
                        d="M43.611 20.083H24v8h11.303c-0.792 2.237-2.231 4.166-4.087 5.571l6.19 5.238C42.048 36.144 44 30.638 44 24c0-1.341-0.138-2.65-0.389-3.917z"
                    />
                </svg>
                Continue with Google
            </button>
        </div>
    );
};

export default Auth;
