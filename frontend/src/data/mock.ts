// Mock data for Tolu Shekoni's AI Portfolio
import { ChatMessage, Project, SkillCategory } from '../types';

interface ChatConversation {
  id: number;
  question: string;
  answer: string;
}

interface SkillsData {
  aiGeneralist: SkillCategory;
  fullStack: SkillCategory;
  processOptimization: SkillCategory;
  devOps: SkillCategory;
  bioPharma: SkillCategory;
  dataEngineering: SkillCategory;
}

interface Testimonial {
  id: number;
  name: string;
  role: string;
  content: string;
  avatar: string;
}

export const mockChatConversations: ChatConversation[] = [
  {
    id: 1,
    question: "What's your background in AI?",
    answer: "I'm passionate about blending my 8+ years in pharmaceutical operations with cutting-edge AI technologies. I've transitioned from optimizing manufacturing processes to building intelligent solutions that transform how organizations solve complex problems."
  },
  {
    id: 2,
    question: "What technologies do you work with?",
    answer: "I specialize in full-stack development with React, Next.js, Python, and Rust. For AI, I work with LLM integration, prompt engineering, and custom AI automations. I also have deep experience in process optimization and data engineering."
  },
  {
    id: 3,
    question: "Tell me about your career transition from biopharma to AI",
    answer: "My transition wasn't a leap but an evolution. My experience in precision-driven biopharma manufacturing, Lean Six Sigma, and regulatory compliance gave me a unique perspective on quality and systematic problem-solving that I now apply to AI development."
  },
  {
    id: 4,
    question: "What makes you different from other AI developers?",
    answer: "I bring analytical rigor from regulated industries, deep operational excellence experience, and a user-focused approach. I understand both the technical complexity and the human impact of AI solutions."
  },
  {
    id: 5,
    question: "What types of projects do you enjoy most?",
    answer: "I love projects that need out-of-the-box thinking - whether it's automating complex workflows, building interactive web platforms, or pushing AI boundaries. My sweet spot is transforming business complexity into elegant, user-friendly solutions."
  }
];

export const mockSkillsData: SkillsData = {
  aiGeneralist: {
    level: 95,
    skills: ['LLM Integration', 'Prompt Engineering', 'AI Automations', 'Machine Learning']
  },
  fullStack: {
    level: 90,
    skills: ['React/Next.js', 'JavaScript/TypeScript', 'Python', 'Rust/WASM', 'Node.js']
  },
  processOptimization: {
    level: 98,
    skills: ['Lean Six Sigma', 'Data Analytics', 'Workflow Automation', 'Change Management']
  },
  devOps: {
    level: 85,
    skills: ['Docker', 'GitHub Actions', 'Cloud Deployment', 'CI/CD']
  },
  bioPharma: {
    level: 95,
    skills: ['cGMP', 'Technical Troubleshooting', 'Regulatory Compliance', 'Quality Systems']
  },
  dataEngineering: {
    level: 88,
    skills: ['ETL', 'Analytics', 'Data Visualization', 'Decision Support']
  }
};

export const mockProjects: Project[] = [
  {
    id: 1,
    title: "Web3 Portfolio",
    description: "Designed and deployed a cutting-edge blockchain portfolio platform, blending smart contract integrations and decentralized identity for a seamless user experience.",
    technologies: ["React", "Web3.js", "Solidity", "IPFS"],
    image: "https://images.unsplash.com/photo-1639762681485-074b7f938ba0?w=600&h=400&fit=crop",
    github: "#",
    demo: "#",
    featured: true
  },
  {
    id: 2,
    title: "Rust + WASM Editor",
    description: "Created an in-browser code editor leveraging Rust and WASM, maximizing performance and interactivity for next-gen web applications.",
    technologies: ["Rust", "WASM", "JavaScript", "Monaco Editor"],
    image: "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=600&h=400&fit=crop",
    github: "#",
    demo: "#",
    featured: true
  },
  {
    id: 3,
    title: "Spotify Pixel-Perfect Clone",
    description: "Delivered a responsive, visually identical Spotify UI clone with advanced interactivity—showcasing an eye for design and UX.",
    technologies: ["React", "CSS3", "JavaScript", "Responsive Design"],
    image: "https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=600&h=400&fit=crop",
    github: "#",
    demo: "#",
    featured: false
  },
  {
    id: 4,
    title: "Intent Journal",
    description: "Built a minimal, sticky habit-tracking and reflection app—combining cognitive principles and modern web tech to empower positive change.",
    technologies: ["React Native", "SQLite", "Node.js", "Express"],
    image: "https://images.unsplash.com/photo-1484480974693-6ca0a78fb36b?w=600&h=400&fit=crop",
    github: "#",
    demo: "#",
    featured: false
  },
  {
    id: 5,
    title: "QuickChops",
    description: "Engineered an e-commerce and brand site for a family food business, raising conversions through engaging storytelling and zero-friction checkout flows.",
    technologies: ["Next.js", "Stripe", "MongoDB", "Tailwind CSS"],
    image: "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=600&h=400&fit=crop",
    github: "#",
    demo: "#",
    featured: true
  }
];

export const mockTestimonials: Testimonial[] = [
  {
    id: 1,
    name: "Sarah Johnson",
    role: "CTO at TechFlow",
    content: "Tolu's unique background in both regulated industries and AI development brings a level of rigor and innovation that's rare in our field. His solutions are both technically excellent and practically grounded.",
    avatar: "https://images.unsplash.com/photo-1494790108755-2616b612b647?w=100&h=100&fit=crop&crop=face"
  },
  {
    id: 2,
    name: "Marcus Chen",
    role: "Founder at DataVision",
    content: "Working with Tolu was transformative for our automation processes. He doesn't just build solutions—he understands the business context and delivers systems that actually work in the real world.",
    avatar: "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=100&h=100&fit=crop&crop=face"
  },
  {
    id: 3,
    name: "Emma Rodriguez",
    role: "Head of Operations at BioLab",
    content: "Tolu's transition from biopharma to AI isn't just impressive—it's exactly what our industry needs. Someone who understands both the technical possibilities and operational realities.",
    avatar: "https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=100&h=100&fit=crop&crop=face"
  }
];

export const mockContactSubmissions: any[] = [];