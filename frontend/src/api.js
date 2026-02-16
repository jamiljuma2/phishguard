import axios from 'axios';

const api = axios.create({
    baseURL: 'https://phishguard-1-e2r2.onrender.com',
    headers: {
        'Content-Type': 'application/json',
    },
});

export default api;
