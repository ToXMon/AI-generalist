import React, { useEffect, useRef } from 'react';
import { ChevronDown } from 'lucide-react';

const Hero = () => {
  const vantaRef = useRef(null);
  const vantaEffect = useRef(null);

  useEffect(() => {
    // Vanta.js NET effect will be loaded here
    // For now, we'll create a CSS-based neural network animation
    const canvas = vantaRef.current;
    if (canvas) {
      // Create animated particles effect using CSS
      const particles = [];
      for (let i = 0; i < 50; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        particle.style.cssText = `
          position: absolute;
          width: 3px;
          height: 3px;
          background: linear-gradient(45deg, #3b82f6, #8b5cf6);
          border-radius: 50%;
          opacity: 0.7;
          animation: float ${3 + Math.random() * 4}s ease-in-out infinite;
          left: ${Math.random() * 100}%;
          top: ${Math.random() * 100}%;
          animation-delay: ${Math.random() * 2}s;
        `;
        canvas.appendChild(particle);
        particles.push(particle);
      }

      // Create connection lines
      const connections = document.createElement('div');
      connections.className = 'connections';
      connections.innerHTML = `
        <svg width="100%" height="100%" style="position: absolute; top: 0; left: 0;">
          <defs>
            <linearGradient id="lineGradient" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" style="stop-color:#3b82f6;stop-opacity:0.3" />
              <stop offset="50%" style="stop-color:#8b5cf6;stop-opacity:0.6" />
              <stop offset="100%" style="stop-color:#3b82f6;stop-opacity:0.3" />
            </linearGradient>
          </defs>
          ${Array.from({length: 20}, (_, i) => `
            <line 
              x1="${Math.random() * 100}%" 
              y1="${Math.random() * 100}%" 
              x2="${Math.random() * 100}%" 
              y2="${Math.random() * 100}%" 
              stroke="url(#lineGradient)" 
              stroke-width="1" 
              opacity="0.4"
              style="animation: pulse ${2 + Math.random() * 3}s ease-in-out infinite alternate;"
            />
          `).join('')}
        </svg>
      `;
      canvas.appendChild(connections);
    }

    return () => {
      // Cleanup
      if (vantaRef.current) {
        vantaRef.current.innerHTML = '';
      }
    };
  }, []);

  const scrollToAbout = () => {
    document.getElementById('about')?.scrollIntoView({ behavior: 'smooth' });
  };

  return (
    <section className="relative min-h-screen flex items-center justify-center overflow-hidden bg-gradient-to-br from-slate-900 via-blue-900 to-purple-900">
      {/* Animated Neural Network Background */}
      <div 
        ref={vantaRef} 
        className="absolute inset-0 w-full h-full"
        style={{
          background: 'radial-gradient(ellipse at center, rgba(59, 130, 246, 0.15) 0%, transparent 70%)'
        }}
      />

      {/* Content */}
      <div className="relative z-10 text-center px-6 max-w-6xl mx-auto">
        <div className="animate-fade-in-up">
          <h1 className="text-5xl md:text-7xl lg:text-8xl font-light text-white mb-6 leading-tight">
            <span className="bg-gradient-to-r from-blue-400 via-purple-400 to-blue-400 bg-clip-text text-transparent animate-gradient-x">
              AI Generalist
            </span>
          </h1>
          
          <div className="text-xl md:text-2xl lg:text-3xl text-gray-300 mb-8 max-w-4xl mx-auto font-light leading-relaxed">
            A relentless problem solver, building the future with{' '}
            <span className="text-blue-400 font-medium">AI</span>, {' '}
            <span className="text-purple-400 font-medium">code</span>, and {' '}
            <span className="text-blue-400 font-medium">continuous improvement</span>.
          </div>

          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center mb-16">
            <button 
              onClick={scrollToAbout}
              className="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-8 py-4 rounded-full text-lg font-medium hover:shadow-xl hover:shadow-blue-500/25 transform hover:-translate-y-1 transition-all duration-300"
            >
              Explore My Work
            </button>
            <button 
              onClick={() => document.getElementById('ai-chat')?.scrollIntoView({ behavior: 'smooth' })}
              className="border border-white/30 text-white px-8 py-4 rounded-full text-lg font-medium hover:bg-white/10 hover:border-white/50 transition-all duration-300"
            >
              Chat with AI Me
            </button>
          </div>
        </div>
      </div>

      {/* Scroll Indicator */}
      <div className="absolute bottom-8 left-1/2 transform -translate-x-1/2 animate-bounce">
        <button 
          onClick={scrollToAbout}
          className="text-white/70 hover:text-white transition-colors duration-300"
        >
          <ChevronDown size={32} />
        </button>
      </div>

      {/* CSS Animations */}
      <style jsx>{`
        @keyframes float {
          0%, 100% { transform: translateY(0px) rotate(0deg); }
          50% { transform: translateY(-20px) rotate(180deg); }
        }
        
        @keyframes pulse {
          0% { opacity: 0.2; }
          100% { opacity: 0.8; }
        }
        
        @keyframes fade-in-up {
          0% {
            opacity: 0;
            transform: translateY(40px);
          }
          100% {
            opacity: 1;
            transform: translateY(0);
          }
        }
        
        @keyframes gradient-x {
          0%, 100% {
            background-size: 200% 200%;
            background-position: left center;
          }
          50% {
            background-size: 200% 200%;
            background-position: right center;
          }
        }
        
        .animate-fade-in-up {
          animation: fade-in-up 1s ease-out;
        }
        
        .animate-gradient-x {
          animation: gradient-x 4s ease infinite;
        }
      `}</style>
    </section>
  );
};

export default Hero;