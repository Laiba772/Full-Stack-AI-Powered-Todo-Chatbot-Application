// lib/api/clients.ts
import axios from 'axios';

const apiClient = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'https://laiba67-todo-app.hf.space/api',
  withCredentials: true,           // ← very important for cookies
  headers: {
    'Content-Type': 'application/json',
  },
});

export default apiClient;