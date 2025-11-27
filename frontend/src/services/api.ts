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

// Stream event types for SSE parsing
export interface StreamMetadata {
  session_id: string;
  query_type: string;
  model: string;
}

export interface StreamToken {
  type: 'token';
  content: string;
}

export interface StreamEvent {
  type: 'metadata' | 'token' | 'done' | 'error';
  [key: string]: any;
}

export const chatAPI = {
  sendMessage: async (chatRequest: ChatRequest): Promise<ChatResponse> => {
    const response: AxiosResponse<ChatResponse> = await api.post('/chat', chatRequest);
    return response.data;
  },

  /**
   * Stream chat response using Server-Sent Events
   * Yields tokens in real-time as they're generated
   */
  streamMessage: async function* (chatRequest: ChatRequest): AsyncGenerator<StreamEvent> {
    const response = await fetch('/api/chat/stream', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(chatRequest),
    });

    if (!response.ok) {
      throw new Error(`Stream error: ${response.status} ${response.statusText}`);
    }

    const reader = response.body?.getReader();
    if (!reader) {
      throw new Error('Response body is not readable');
    }

    const decoder = new TextDecoder();
    let buffer = '';

    try {
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n');
        
        // Keep the last incomplete line in the buffer
        buffer = lines[lines.length - 1];

        for (let i = 0; i < lines.length - 1; i++) {
          const line = lines[i].trim();
          
          if (line.startsWith('data: ')) {
            try {
              const event: StreamEvent = JSON.parse(line.slice(6));
              yield event;
            } catch (e) {
              console.error('Failed to parse SSE event:', line, e);
            }
          }
        }
      }
    } finally {
      reader.releaseLock();
    }
  },

  /**
   * Get chat session statistics
   */
  getSessionStats: async (sessionId: string): Promise<any> => {
    const response = await api.get(`/chat/stats/${sessionId}`);
    return response.data;
  },

  /**
   * Clear a chat session
   */
  clearSession: async (sessionId: string): Promise<any> => {
    const response = await api.delete(`/chat/${sessionId}`);
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