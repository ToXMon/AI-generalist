import React, { useState, useRef, useEffect } from 'react';
import { Send, Bot, User, Minimize2, Maximize2, Sparkles } from 'lucide-react';
import { chatAPI } from '../services/api';
import { ChatMessage, ChatRequest } from '../types';
import DOMPurify from 'dompurify';

const AIChat: React.FC = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: 1,
      type: 'ai',
      content: "Hi! I'm an AI assistant powered by Venice AI. I'm here to help answer your questions and provide information. What can I help you with today?",
      timestamp: new Date()
    }
  ]);
  const [inputMessage, setInputMessage] = useState<string>('');
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [isMinimized, setIsMinimized] = useState<boolean>(false);
  const [sessionId, setSessionId] = useState<string | undefined>(undefined);
  const [error, setError] = useState<string | null>(null);
  const [isInitialLoad, setIsInitialLoad] = useState<boolean>(true);
  const [hasLoadedFromStorage, setHasLoadedFromStorage] = useState<boolean>(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = (): void => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    // Only scroll to bottom if:
    // 1. Not initial load AND
    // 2. We've already loaded messages from storage AND
    // 3. There are actually new messages (length increased from previous)
    if (!isInitialLoad && hasLoadedFromStorage) {
      // Add a small delay to ensure this doesn't interfere with page-level scrolling
      const timeoutId = setTimeout(() => {
        scrollToBottom();
      }, 50);
      
      return () => clearTimeout(timeoutId);
    }
  }, [messages, isInitialLoad, hasLoadedFromStorage]);

  // Load session from localStorage on component mount
  useEffect(() => {
    const loadSession = () => {
      const savedSession = localStorage.getItem('aiChatSession');
      if (savedSession) {
        try {
          const sessionData = JSON.parse(savedSession);
          if (sessionData.sessionId) {
            setSessionId(sessionData.sessionId);
          }
          if (sessionData.messages && sessionData.messages.length > 1) {
            // Convert timestamp strings back to Date objects
            const messagesWithDates = sessionData.messages.map((msg: any) => ({
              ...msg,
              timestamp: new Date(msg.timestamp)
            }));
            setMessages(messagesWithDates);
          }
        } catch (error) {
          console.error('Failed to load chat session:', error);
        }
      }
      // Mark that we've loaded from storage and initial load is complete
      setHasLoadedFromStorage(true);
      setIsInitialLoad(false);
    };

    // Use a small timeout to ensure the component is fully mounted
    const timeoutId = setTimeout(loadSession, 100);
    
    return () => clearTimeout(timeoutId);
  }, []);

  // Save session to localStorage whenever messages change
  useEffect(() => {
    if (sessionId && messages.length > 1) {
      const sessionData = {
        sessionId,
        messages
      };
      localStorage.setItem('aiChatSession', JSON.stringify(sessionData));
    }
  }, [messages, sessionId]);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>): void => {
    setInputMessage(e.target.value);
    // Clear error when user starts typing
    if (error) {
      setError(null);
    }
  };

  const handleSendMessage = async (e: React.FormEvent<HTMLFormElement>): Promise<void> => {
    e.preventDefault();
    if (!inputMessage.trim()) return;

    setError(null);

    // Add user message
    const userMessage: ChatMessage = {
      id: Date.now(),
      type: 'user',
      content: inputMessage,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);

    try {
      // Call backend API
      const requestData: ChatRequest = {
        message: inputMessage,
        sessionId
      };
      const response = await chatAPI.sendMessage(requestData);

      // Set session ID from response if not already set
      if (!sessionId) {
        setSessionId(response.sessionId);
      }

      // Add AI response
      const aiMessage: ChatMessage = {
        id: Date.now() + 1,
        type: 'ai',
        content: response.response,
        timestamp: new Date(response.timestamp)
      };

      setMessages(prev => [...prev, aiMessage]);

    } catch (error: any) {
      console.error('Chat error:', error);

      // Extract error message safely
      let errorMessage = "I'm sorry, I'm having trouble connecting to my AI brain right now.";
      
      if (error?.response?.data?.detail) {
        errorMessage = error.response.data.detail;
      } else if (error?.message) {
        errorMessage = error.message;
      } else if (typeof error === 'string') {
        errorMessage = error;
      }

      // Add error message to chat
      const errorChatMessage: ChatMessage = {
        id: Date.now() + 1,
        type: 'ai',
        content: `${errorMessage} Please try again later or contact Tolu directly if the issue persists!`,
        timestamp: new Date()
      };

      setMessages(prev => [...prev, errorChatMessage]);
      
      // Set user-friendly error for display
      const displayError = error?.response?.status === 504 
        ? "Venice AI service is temporarily unavailable" 
        : error?.response?.status === 503
        ? "Unable to connect to AI service"
        : "Failed to get AI response";
        
      setError(displayError);
    } finally {
      setIsLoading(false);
    }
  };

  const formatTime = (timestamp: Date): string => {
    return new Intl.DateTimeFormat('en', {
      hour: 'numeric',
      minute: '2-digit',
      hour12: true
    }).format(timestamp);
  };

  const suggestedQuestions: string[] = [
    "What's your background in AI?",
    "Tell me about your career transition",
    "What technologies do you work with?",
    "What makes you different from other developers?"
  ];

  const handleSuggestionClick = (question: string): void => {
    setInputMessage(question);
  };

  return (
    <section id="ai-chat" className="py-24 bg-gradient-to-br from-blue-50 to-purple-50">
      <div className="container mx-auto px-6 max-w-4xl">
        {/* Section Header */}
        <div className="text-center mb-12">
          <h2 className="text-4xl md:text-5xl font-light text-gray-900 mb-6">
            Chat with AI <span className="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent font-medium">Tolu</span>
          </h2>
          <div className="w-24 h-1 bg-gradient-to-r from-blue-600 to-purple-600 mx-auto rounded-full mb-4"></div>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Ask me anything about my background, skills, projects, or career journey. I'm powered by Venice AI to give you detailed insights!
          </p>
        </div>

        {/* Chat Interface */}
        <div className="bg-white rounded-3xl shadow-xl overflow-hidden border border-gray-200">
          {/* Chat Header */}
          <div className="bg-gradient-to-r from-blue-600 to-purple-600 p-4 text-white">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <div className="w-10 h-10 bg-white/20 rounded-full flex items-center justify-center">
                  <Bot size={20} />
                </div>
                <div>
                  <h3 className="font-semibold">AI Tolu Assistant</h3>
                  <p className="text-blue-100 text-sm">Powered by Venice AI</p>
                </div>
              </div>
              <button
                onClick={() => setIsMinimized(!isMinimized)}
                className="p-2 hover:bg-white/20 rounded-lg transition-colors duration-200"
              >
                {isMinimized ? <Maximize2 size={18} /> : <Minimize2 size={18} />}
              </button>
            </div>
          </div>

          {/* Chat Messages */}
          {!isMinimized && (
            <>
              <div className="h-96 overflow-y-auto p-6 space-y-4">
                {messages.map((message) => (
                  <div
                    key={message.id}
                    className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
                  >
                    <div className={`flex items-start space-x-3 max-w-xs md:max-w-md lg:max-w-lg ${
                      message.type === 'user' ? 'flex-row-reverse space-x-reverse' : ''
                    }`}>
                      {/* Avatar */}
                      <div className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 ${
                        message.type === 'user'
                          ? 'bg-gradient-to-r from-blue-600 to-purple-600'
                          : 'bg-gradient-to-r from-purple-600 to-pink-600'
                      }`}>
                        {message.type === 'user' ? (
                          <User size={16} className="text-white" />
                        ) : (
                          <Bot size={16} className="text-white" />
                        )}
                      </div>

                      {/* Message Bubble */}
                      <div className={`rounded-2xl px-4 py-3 ${
                        message.type === 'user'
                          ? 'bg-gradient-to-r from-blue-600 to-purple-600 text-white'
                          : 'bg-gray-100 text-gray-800'
                      }`}>
                        <p className="text-sm leading-relaxed">{DOMPurify.sanitize(message.content, { ALLOWED_TAGS: [] })}</p>
                        <p className={`text-xs mt-2 ${
                          message.type === 'user' ? 'text-blue-100' : 'text-gray-500'
                        }`}>
                          {formatTime(message.timestamp)}
                        </p>
                      </div>
                    </div>
                  </div>
                ))}

                {/* Loading Indicator */}
                {isLoading && (
                  <div className="flex justify-start">
                    <div className="flex items-start space-x-3">
                      <div className="w-8 h-8 bg-gradient-to-r from-purple-600 to-pink-600 rounded-full flex items-center justify-center">
                        <Bot size={16} className="text-white" />
                      </div>
                      <div className="bg-gray-100 rounded-2xl px-4 py-3">
                        <div className="flex space-x-1">
                          <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                          <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
                          <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
                        </div>
                      </div>
                    </div>
                  </div>
                )}

                <div ref={messagesEndRef} />
              </div>

              {/* Error Message */}
              {error && (
                <div className="px-6 pb-2">
                  <div className="bg-red-50 border border-red-200 rounded-lg p-3">
                    <p className="text-red-600 text-sm">{error}</p>
                  </div>
                </div>
              )}

              {/* Suggested Questions */}
              {messages.length === 1 && (
                <div className="px-6 pb-4">
                  <p className="text-sm text-gray-500 mb-3 flex items-center">
                    <Sparkles size={16} className="mr-2" />
                    Try asking:
                  </p>
                  <div className="flex flex-wrap gap-2">
                    {suggestedQuestions.map((question, index) => (
                      <button
                        key={index}
                        onClick={() => handleSuggestionClick(question)}
                        className="bg-gradient-to-r from-blue-50 to-purple-50 hover:from-blue-100 hover:to-purple-100 text-gray-700 px-3 py-2 rounded-full text-sm transition-all duration-200 border border-gray-200 hover:border-blue-300"
                      >
                        {question}
                      </button>
                    ))}
                  </div>
                </div>
              )}

              {/* Chat Input */}
              <div className="border-t border-gray-200 p-4">
                <form onSubmit={handleSendMessage} className="flex space-x-3">
                  <input
                    type="text"
                    value={inputMessage}
                    onChange={handleInputChange}
                    placeholder="Ask me anything about Tolu's background, skills, or projects..."
                    className="flex-1 border border-gray-300 rounded-full px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    disabled={isLoading}
                  />
                  <button
                    type="submit"
                    disabled={isLoading || !inputMessage.trim()}
                    className="bg-gradient-to-r from-blue-600 to-purple-600 text-white p-2 rounded-full hover:shadow-lg transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    <Send size={18} />
                  </button>
                </form>
              </div>
            </>
          )}
        </div>

        {/* AI Status */}
        <div className="text-center mt-8">
          <p className="text-gray-500 text-sm">
            🤖 Powered by Venice AI • {sessionId ? `Session: ${sessionId.slice(0, 8)}...` : 'Starting new session'}
          </p>
        </div>
      </div>
    </section>
  );
};

export default AIChat;