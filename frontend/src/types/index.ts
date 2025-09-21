// TypeScript interfaces for Tolu Shekoni Portfolio

export interface ChatMessage {
  id: number;
  type: 'user' | 'ai';
  content: string;
  timestamp: Date;
}

export interface ChatRequest {
  message: string;
  sessionId?: string;
}

export interface ChatResponse {
  response: string;
  sessionId: string;
  timestamp: string;
}

export interface ContactForm {
  name: string;
  email: string;
  company?: string;
  subject: string;
  message: string;
}

export interface ContactResponse {
  success: boolean;
  messageId?: string;
  error?: string;
}

export interface Project {
  id: number;
  title: string;
  description: string;
  technologies: string[];
  image: string;
  github: string;
  demo: string;
  featured: boolean;
}

export interface SkillCategory {
  level: number;
  skills: string[];
}

export interface SkillsData {
  aiGeneralist: SkillCategory;
  fullStack: SkillCategory;
  processOptimization: SkillCategory;
  devOps: SkillCategory;
  bioPharma: SkillCategory;
  dataEngineering: SkillCategory;
}

export interface Testimonial {
  id: number;
  name: string;
  role: string;
  content: string;
  avatar: string;
}

export interface ApiError {
  detail: string;
}

export interface SessionStorage {
  sessionId?: string;
  messages?: ChatMessage[];
}