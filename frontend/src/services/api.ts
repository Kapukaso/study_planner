import axios from 'axios';

const api = axios.create({
  baseURL: '', // Using relative path for Vite proxy
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add interceptor for auth token if needed
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;
