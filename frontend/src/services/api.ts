// API service layer for Tolu Shekoni Portfolio
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const api = axios.create({
  baseURL: `${BACKEND_URL}/api`,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

export const chatAPI = {
  sendMessage: async (chatRequest) => {
    const response = await api.post('/chat', chatRequest);
    return response.data;
  },
};

export const contactAPI = {
  submitForm: async (contactData) => {
    const response = await api.post('/contact', contactData);
    return response.data;
  },
};

export const healthAPI = {
  checkStatus: async () => {
    const response = await api.get('/');
    return response.data;
  },
};

export default api;