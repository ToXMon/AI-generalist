// API service layer for Tolu Shekoni Portfolio
import axios, { AxiosResponse } from 'axios';
import { ChatRequest, ChatResponse, ContactForm, ContactResponse } from '../types';

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
  sendMessage: async (chatRequest: ChatRequest): Promise<ChatResponse> => {
    const response: AxiosResponse<ChatResponse> = await api.post('/chat', chatRequest);
    return response.data;
  },
};

export const contactAPI = {
  submitForm: async (contactData: ContactForm): Promise<ContactResponse> => {
    const response: AxiosResponse<ContactResponse> = await api.post('/contact', contactData);
    return response.data;
  },
};

export const healthAPI = {
  checkStatus: async (): Promise<{ message: string }> => {
    const response: AxiosResponse<{ message: string }> = await api.get('/');
    return response.data;
  },
};

export default api;