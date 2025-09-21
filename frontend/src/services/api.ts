// API service layer for Tolu Shekoni Portfolio
import axios, { AxiosResponse } from 'axios';
import { ChatRequest, ChatResponse, ContactForm, ContactResponse } from '../types';

const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add response interceptor for error handling
api.interceptors.response.use(
  (response: AxiosResponse) => response,
  (error: any) => {
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
  checkStatus: async (): Promise<any> => {
    const response: AxiosResponse<any> = await api.get('/');
    return response.data;
  },
};

export default api;