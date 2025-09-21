import React from 'react';
import { Heart, Code, Brain, Linkedin, Mail, ExternalLink } from 'lucide-react';

const Footer: React.FC = () => {
  const currentYear: number = new Date().getFullYear();

  const scrollToSection = (sectionId: string): void => {
    const element = document.getElementById(sectionId);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  };

  const scrollToTop = (): void => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  return (
    <footer className="bg-gray-900 text-white">
      <div className="container mx-auto px-6 py-12 max-w-6xl">
        <div className="grid md:grid-cols-4 gap-8">
          {/* Brand */}
          <div className="md:col-span-2">
            <div className="flex items-center space-x-3 mb-6">
              <div className="w-10 h-10 bg-gradient-to-r from-blue-600 to-purple-600 rounded-xl flex items-center justify-center">
                <Brain className="text-white" size={20} />
              </div>
              <h3 className="text-xl font-bold">Tolu Shekoni</h3>
            </div>
            <p className="text-gray-400 leading-relaxed mb-6 max-w-md">
              AI Generalist and Full-Stack Developer passionate about transforming complex challenges into elegant solutions. From biopharma operations to cutting-edge AI development.
            </p>
            <div className="flex space-x-4">
              <a
                href="mailto:tolu.a.shekoni@gmail.com"
                className="w-10 h-10 bg-gray-800 hover:bg-gradient-to-r hover:from-blue-600 hover:to-purple-600 rounded-lg flex items-center justify-center transition-all duration-300 hover:shadow-lg"
              >
                <Mail size={18} />
              </a>
              <a
                href="https://www.linkedin.com/in/tolulope-shekoni-23542063"
                target="_blank"
                rel="noopener noreferrer"
                className="w-10 h-10 bg-gray-800 hover:bg-gradient-to-r hover:from-blue-600 hover:to-purple-600 rounded-lg flex items-center justify-center transition-all duration-300 hover:shadow-lg"
              >
                <Linkedin size={18} />
              </a>
            </div>
          </div>

          {/* Quick Links */}
          <div>
            <h4 className="text-lg font-semibold mb-4">Quick Links</h4>
            <nav className="space-y-3">
              {[
                { label: 'About', id: 'about' },
                { label: 'Skills', id: 'skills' },
                { label: 'Projects', id: 'projects' },
                { label: 'AI Chat', id: 'ai-chat' },
                { label: 'Contact', id: 'contact' }
              ].map((link) => (
                <button
                  key={link.id}
                  onClick={() => scrollToSection(link.id)}
                  className="block text-gray-400 hover:text-white transition-colors duration-200"
                >
                  {link.label}
                </button>
              ))}
            </nav>
          </div>

          {/* Expertise */}
          <div>
            <h4 className="text-lg font-semibold mb-4">Expertise</h4>
            <div className="space-y-3">
              {[
                'AI Integration',
                'Full-Stack Development',
                'Process Optimization',
                'Rust/WASM',
                'Data Analytics',
                'DevOps & Cloud'
              ].map((skill) => (
                <div key={skill} className="flex items-center space-x-2">
                  <div className="w-2 h-2 bg-gradient-to-r from-blue-600 to-purple-600 rounded-full"></div>
                  <span className="text-gray-400 text-sm">{skill}</span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Divider */}
        <div className="border-t border-gray-800 mt-12 pt-8">
          <div className="flex flex-col md:flex-row justify-between items-center space-y-4 md:space-y-0">
            {/* Copyright */}
            <div className="flex items-center space-x-2 text-gray-400">
              <span>© {currentYear} Tolu Shekoni. Built with</span>
              <Heart size={16} className="text-red-500 mx-1" />
              <span>and</span>
              <Code size={16} className="text-blue-400 mx-1" />
            </div>

            {/* Back to Top */}
            <button
              onClick={scrollToTop}
              className="flex items-center space-x-2 text-gray-400 hover:text-white transition-colors duration-200 group"
            >
              <span>Back to Top</span>
              <ExternalLink size={16} className="transform rotate-45 group-hover:-translate-y-1 transition-transform duration-200" />
            </button>
          </div>

          {/* Tech Stack Note */}
          <div className="text-center mt-6">
            <p className="text-gray-500 text-sm">
              Powered by React, Tailwind CSS, and Venice AI • Deployed on Akash Network
            </p>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;