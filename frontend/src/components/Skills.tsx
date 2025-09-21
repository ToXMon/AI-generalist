import React, { useState, useEffect, useRef } from 'react';
import { Brain, Code, Cog, Cloud, Beaker, Database, LucideIcon } from 'lucide-react';
import { mockSkillsData } from '../data/mock';
import { SkillCategory } from '../types';

const Skills: React.FC = () => {
  const [isVisible, setIsVisible] = useState<boolean>(false);
  const sectionRef = useRef<HTMLElement>(null);

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setIsVisible(true);
        }
      },
      { threshold: 0.3 }
    );

    if (sectionRef.current) {
      observer.observe(sectionRef.current);
    }

    return () => observer.disconnect();
  }, []);

  const skillCategories = [
    {
      title: 'AI Generalist',
      icon: Brain,
      color: 'from-purple-500 to-pink-500',
      data: mockSkillsData.aiGeneralist,
      bgColor: 'bg-purple-50'
    },
    {
      title: 'Full-Stack Development',
      icon: Code,
      color: 'from-blue-500 to-cyan-500',
      data: mockSkillsData.fullStack,
      bgColor: 'bg-blue-50'
    },
    {
      title: 'Process Optimization',
      icon: Cog,
      color: 'from-green-500 to-emerald-500',
      data: mockSkillsData.processOptimization,
      bgColor: 'bg-green-50'
    },
    {
      title: 'DevOps & Cloud',
      icon: Cloud,
      color: 'from-orange-500 to-red-500',
      data: mockSkillsData.devOps,
      bgColor: 'bg-orange-50'
    },
    {
      title: 'BioPharma Ops',
      icon: Beaker,
      color: 'from-indigo-500 to-purple-500',
      data: mockSkillsData.bioPharma,
      bgColor: 'bg-indigo-50'
    },
    {
      title: 'Data Engineering',
      icon: Database,
      color: 'from-teal-500 to-blue-500',
      data: mockSkillsData.dataEngineering,
      bgColor: 'bg-teal-50'
    }
  ];

  return (
    <section id="skills" ref={sectionRef} className="py-24 bg-white">
      <div className="container mx-auto px-6 max-w-6xl">
        {/* Section Header */}
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-light text-gray-900 mb-6">
            My <span className="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent font-medium">Skills</span>
          </h2>
          <div className="w-24 h-1 bg-gradient-to-r from-blue-600 to-purple-600 mx-auto rounded-full mb-4"></div>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            A unique blend of technical expertise, operational excellence, and AI innovation
          </p>
        </div>

        {/* Skills Grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          {skillCategories.map((category, index) => {
            const IconComponent: LucideIcon = category.icon;

            return (
              <div
                key={category.title}
                className={`${category.bgColor} rounded-2xl p-6 hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1`}
                style={{
                  animationDelay: `${index * 100}ms`
                }}
              >
                {/* Icon and Title */}
                <div className="flex items-center mb-6">
                  <div className={`w-12 h-12 bg-gradient-to-r ${category.color} rounded-xl flex items-center justify-center mr-4`}>
                    <IconComponent className="text-white" size={24} />
                  </div>
                  <h3 className="text-xl font-semibold text-gray-900">{category.title}</h3>
                </div>

                {/* Progress Bar */}
                <div className="mb-6">
                  <div className="flex justify-between items-center mb-2">
                    <span className="text-sm text-gray-600">Proficiency</span>
                    <span className="text-sm font-semibold text-gray-900">{category.data.level}%</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div
                      className={`h-2 bg-gradient-to-r ${category.color} rounded-full transition-all duration-1000 ease-out`}
                      style={{
                        width: isVisible ? `${category.data.level}%` : '0%'
                      }}
                    />
                  </div>
                </div>

                {/* Skills List */}
                <div className="space-y-2">
                  {category.data.skills.map((skill, skillIndex) => (
                    <div
                      key={skill}
                      className="flex items-center text-gray-700"
                      style={{
                        opacity: isVisible ? 1 : 0,
                        transform: isVisible ? 'translateX(0)' : 'translateX(-20px)',
                        transition: `all 0.6s ease-out ${(skillIndex * 100) + 300}ms`
                      }}
                    >
                      <div className={`w-2 h-2 bg-gradient-to-r ${category.color} rounded-full mr-3`}></div>
                      <span className="text-sm">{skill}</span>
                    </div>
                  ))}
                </div>
              </div>
            );
          })}
        </div>

        {/* Skills Summary */}
        <div className="mt-16 text-center">
          <div className="bg-gradient-to-r from-gray-50 to-blue-50 rounded-2xl p-8">
            <h3 className="text-2xl font-semibold text-gray-900 mb-4">Core Competencies</h3>
            <div className="flex flex-wrap justify-center gap-3">
              {[
                'LLM Integration', 'Prompt Engineering', 'React/Next.js', 'Python', 'Rust/WASM',
                'Lean Six Sigma', 'Data Analytics', 'Docker', 'cGMP', 'Process Automation'
              ].map((skill) => (
                <span
                  key={skill}
                  className="bg-white px-4 py-2 rounded-full text-sm font-medium text-gray-700 shadow-sm hover:shadow-md transition-shadow duration-200"
                >
                  {skill}
                </span>
              ))}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Skills;