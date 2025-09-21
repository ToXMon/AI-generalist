import React from 'react';
import { Code, Brain, Zap, Target } from 'lucide-react';

const About: React.FC = () => {
  return (
    <section id="about" className="py-24 bg-gray-50">
      <div className="container mx-auto px-6 max-w-6xl">
        {/* Section Header */}
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-light text-gray-900 mb-6">
            About <span className="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent font-medium">Me</span>
          </h2>
          <div className="w-24 h-1 bg-gradient-to-r from-blue-600 to-purple-600 mx-auto rounded-full"></div>
        </div>

        <div className="grid lg:grid-cols-2 gap-16 items-center">
          {/* Content */}
          <div className="space-y-6">
            <p className="text-lg text-gray-700 leading-relaxed">
              I'm <span className="font-semibold text-gray-900">Tolu Shekoni</span>, a relentless problem solver blending 8+ years in operational and technical roles within pharmaceutical manufacturing with a passion for crafting digital solutions using AI and code.
            </p>

            <p className="text-lg text-gray-700 leading-relaxed">
              My mission? Use advanced technologies to deliver meaningful impact—automating processes, driving efficiency, and enabling others to thrive with intelligent solutions.
            </p>

            <p className="text-lg text-gray-700 leading-relaxed">
              Previously, I transformed commercial and GMP operations at global biopharma organizations through Lean, Six Sigma, and change management. Now, I help teams, founders, and organizations accelerate with full-stack development and AI, turning complexity into clarity—one project at a time.
            </p>

            {/* Stats */}
            <div className="grid grid-cols-2 gap-6 mt-8">
              <div className="text-center p-4 bg-white rounded-xl shadow-sm">
                <div className="text-3xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">8+</div>
                <div className="text-gray-600 text-sm">Years Experience</div>
              </div>
              <div className="text-center p-4 bg-white rounded-xl shadow-sm">
                <div className="text-3xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">50+</div>
                <div className="text-gray-600 text-sm">Projects Delivered</div>
              </div>
            </div>
          </div>

          {/* Visual Elements */}
          <div className="relative">
            {/* Main Image Placeholder */}
            <div className="relative bg-gradient-to-br from-blue-100 to-purple-100 rounded-2xl p-8 h-96 flex items-center justify-center">
              <div className="text-center">
                <div className="w-32 h-32 bg-gradient-to-r from-blue-600 to-purple-600 rounded-full mx-auto mb-4 flex items-center justify-center">
                  <Brain size={48} className="text-white" />
                </div>
                <p className="text-gray-700 font-medium">AI + Operations Expert</p>
              </div>
            </div>

            {/* Floating Icons */}
            <div className="absolute -top-4 -right-4 bg-white p-3 rounded-xl shadow-lg animate-bounce" style={{animationDelay: '0s'}}>
              <Code className="text-blue-600" size={24} />
            </div>
            <div className="absolute -bottom-4 -left-4 bg-white p-3 rounded-xl shadow-lg animate-bounce" style={{animationDelay: '1s'}}>
              <Zap className="text-purple-600" size={24} />
            </div>
            <div className="absolute top-1/2 -left-6 bg-white p-3 rounded-xl shadow-lg animate-bounce" style={{animationDelay: '2s'}}>
              <Target className="text-blue-600" size={24} />
            </div>
          </div>
        </div>

        {/* Career Transition Story */}
        <div className="mt-24 bg-gradient-to-br from-blue-600 to-purple-600 rounded-3xl p-8 md:p-12 text-white">
          <h3 className="text-3xl md:text-4xl font-light mb-8 text-center">
            Career Transition <span className="font-medium">Story</span>
          </h3>

          <div className="max-w-4xl mx-auto space-y-6 text-lg leading-relaxed text-blue-50">
            <p>
              After nearly a decade navigating the precision-driven world of biopharmaceutical manufacturing, I discovered my true passion: using technology not just to optimize, but to transform. In my roles as an Operational Excellence and Continuous Improvement Manager, I witnessed firsthand how even the most advanced organizations could be empowered through creative problem-solving, data, and automation.
            </p>

            <p>
              My work in Lean methodologies, project management, and technical operations gave me a robust foundation in efficiency, cross-functional collaboration, and delivering measurable results under strict regulatory environments.
            </p>

            <p>
              Yet, as the landscape of innovation shifted, I found myself increasingly captivated by the power of AI. I realized that artificial intelligence and full-stack development are the next frontier—not only for operational excellence but for empowering people and completely reshaping how organizations solve problems.
            </p>

            <p>
              The shift from biopharma to AI generalist isn't a leap into the unknown; it's an evolution. My experience in technical troubleshooting, regulatory compliance, and orchestrating large-scale change enables me to bring a rare combination of analytical rigor, empathy, and strategic vision to any project.
            </p>

            <p className="text-white font-medium">
              My story is proof: with curiosity, humility, and relentless learning, you can reimagine your impact—no matter the industry.
            </p>
          </div>
        </div>
      </div>
    </section>
  );
};

export default About;