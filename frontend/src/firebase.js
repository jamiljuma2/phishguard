// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
import { getAuth } from "firebase/auth";

// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyACe3ich3ACB56VeqSsF3B7leixlmhDVxM",
  authDomain: "phish-guard-94030.firebaseapp.com",
  projectId: "phish-guard-94030",
  storageBucket: "phish-guard-94030.firebasestorage.app",
  messagingSenderId: "675770018478",
  appId: "1:675770018478:web:a605e65ad3d0943fdf5b3f",
  measurementId: "G-RPGYBQTELG"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
export const auth = getAuth(app);
