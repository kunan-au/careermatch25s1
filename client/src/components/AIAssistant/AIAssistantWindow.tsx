import { useState, useRef, useEffect } from 'react';
import { getAIResponse, generateId, AIMessage, isUsingOpenAI } from '@/services/aiService';
import './AIAssistantWindow.css';
import EnvDebugger from './EnvDebugger';

const AIAssistantWindow = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<AIMessage[]>([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isOperating, setIsOperating] = useState(false);
  const [openAIStatus, setOpenAIStatus] = useState<'connected' | 'disconnected' | 'unknown'>('unknown');
  const [showRating, setShowRating] = useState(false);
  const [conversationRating, setConversationRating] = useState<'thumbsUp' | 'thumbsDown' | null>(null);
  const [showEndRating, setShowEndRating] = useState(false);
  const [sessionCount, setSessionCount] = useState(0);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  // Check OpenAI connection status
  useEffect(() => {
    const checkOpenAIStatus = async () => {
      const status = await isUsingOpenAI();
      setOpenAIStatus(status ? 'connected' : 'disconnected');
    };
    
    checkOpenAIStatus();
  }, []);

  // Initial welcome message or new session message
  useEffect(() => {
    if ((messages.length === 0 || sessionCount > 0) && isOpen) {
      const welcomeMessage = {
        id: generateId(),
        text: 'Hello! I am the CareerMatch AI assistant. I can help you learn about platform features, answer questions, or provide usage suggestions. How can I assist you today?',
        isUser: false,
        timestamp: new Date(),
        label: 'AI agent',
        isNewSession: sessionCount > 0
      };
      
      setMessages(prev => {
        // If this is a new session after closing, add the welcome message to existing messages
        if (sessionCount > 0) {
          return [...prev, welcomeMessage];
        }
        // If this is the first time opening, just set the welcome message
        return [welcomeMessage];
      });
    }
  }, [isOpen, sessionCount]);

  // Auto-scroll to latest message
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Focus input when chat window opens
  useEffect(() => {
    if (isOpen) {
      inputRef.current?.focus();
    }
  }, [isOpen]);

  // Check if the message is a closing statement
  const isClosingStatement = (message: string) => {
    const closingKeywords = [
      'thank you', 'thanks', 'thx', 'ty',
      'okay', 'ok', 'alright', 'got it',
      'bye', 'goodbye', 'see you', 'farewell',
      'that\'s all', 'that is all', 'that\'s it', 'that is it'
    ];
    
    // Convert to lowercase and check if message contains any closing keywords
    const lowerMessage = message.toLowerCase();
    return closingKeywords.some(keyword => 
      lowerMessage === keyword || 
      lowerMessage.includes(` ${keyword}`) || 
      lowerMessage.includes(`${keyword} `) ||
      lowerMessage.startsWith(keyword) ||
      lowerMessage.endsWith(keyword)
    );
  };

  const toggleChat = () => {
    // If we're closing the chat
    if (isOpen) {
      setIsOpen(false);
      setConversationRating(null);
      setShowRating(false);
      setShowEndRating(false);
      
      // When we reopen, we'll increment the session counter
      // This will trigger the effect to add a new welcome message
    } else {
      // We're opening the chat
      setIsOpen(true);
      setSessionCount(prev => prev + 1);
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setInputMessage(e.target.value);
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && inputMessage.trim()) {
      sendMessage();
    }
  };

  const sendMessage = async () => {
    if (!inputMessage.trim()) return;

    // Check if the message is a closing statement
    const isClosing = isClosingStatement(inputMessage);

    const userMessage: AIMessage = {
      id: generateId(),
      text: inputMessage,
      isUser: true,
      timestamp: new Date()
    };

    // Update message list, add user message
    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);
    setIsOperating(true);

    try {
      // Show "Agent operating..." status
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      // Get AI response
      const aiResponseText = await getAIResponse(inputMessage);

      // Add AI response to message list
      const aiMessage: AIMessage = {
        id: generateId(),
        text: aiResponseText,
        isUser: false,
        timestamp: new Date(),
        label: 'AI agent'
      };

      setMessages(prev => [...prev, aiMessage]);
      
      // If this was a response to a closing statement, show the rating prompt
      if (isClosing) {
        setShowEndRating(true);
      }
    } catch (error) {
      console.error('Failed to send message:', error);
      
      // Add error message
      const errorMessage: AIMessage = {
        id: generateId(),
        text: 'Sorry, I encountered a problem and cannot respond to your request. Please try again later.',
        isUser: false,
        timestamp: new Date(),
        label: 'AI agent'
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
      setIsOperating(false);
    }
  };

  const handleTransferToHuman = () => {
    // Add transfer message
    const transferMessage: AIMessage = {
      id: generateId(),
      text: 'Please wait, connecting you to a human agent...',
      isUser: false,
      timestamp: new Date(),
      label: 'AI agent'
    };

    setMessages(prev => [...prev, transferMessage]);
    
    // Simulate waiting for human agent
    setTimeout(() => {
      const humanMessage: AIMessage = {
        id: generateId(),
        text: 'Hello, I am John from customer service. How may I help you today?',
        isUser: false,
        timestamp: new Date(),
        label: 'Customer Service'
      };
      
      setMessages(prev => [...prev, humanMessage]);
    }, 2000);
  };

  const toggleRating = () => {
    setShowRating(!showRating);
  };

  const handleRateConversation = (rating: 'thumbsUp' | 'thumbsDown') => {
    setConversationRating(rating);
    setShowRating(false);
    setShowEndRating(false);
    
    // Here you could send the rating to your backend
    console.log(`User rated conversation: ${rating}`);
    
    // No longer adding a new message, instead we'll show feedback text in the UI
  };

  // Format time
  const formatTime = (date: Date) => {
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  // Clear conversation
  const clearConversation = () => {
    setMessages([]);
    setSessionCount(0);
    
    // Add a new welcome message
    const welcomeMessage = {
      id: generateId(),
      text: 'Hello! I am the CareerMatch AI assistant. I can help you learn about platform features, answer questions, or provide usage suggestions. How can I assist you today?',
      isUser: false,
      timestamp: new Date(),
      label: 'AI agent'
    };
    
    setMessages([welcomeMessage]);
  };

  return (
    <div className="ai-assistant-container">
      <EnvDebugger />
      {/* Chat button */}
      <button 
        className={`ai-assistant-button ${isOpen ? 'open' : ''}`} 
        onClick={toggleChat}
        aria-label="AI Assistant"
      >
        {isOpen ? (
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
          </svg>
        ) : (
          <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <circle cx="12" cy="8" r="5" />
            <path d="M12 8v0m0 0v0" />
            <path d="M20 15.54V18a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2v-2.46a2 2 0 0 1 .272-1.007l.47-.705a2 2 0 0 1 1.108-.77A18.86 18.86 0 0 1 12 13c2.1 0 4.1.34 6 .975" />
          </svg>
        )}
      </button>

      {/* Chat window */}
      <div className={`ai-assistant-window ${isOpen ? 'open' : ''}`}>
        <div className="ai-assistant-header">
          <div className="ai-assistant-title">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <circle cx="12" cy="12" r="10"></circle>
              <path d="M12 16v-4"></path>
              <path d="M12 8h.01"></path>
            </svg>
            <span>AI Assistant</span>
            {openAIStatus !== 'unknown' && (
              <span className={`openai-status ${openAIStatus}`} title={`OpenAI: ${openAIStatus}`}>
                {openAIStatus === 'connected' ? '• GPT' : '• Mock'}
              </span>
            )}
          </div>
          <div className="ai-assistant-header-actions">
            <button
              className="ai-assistant-clear-chat"
              onClick={clearConversation}
              title="Clear conversation"
            >
              <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                <path d="M3 6h18"></path>
                <path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"></path>
                <path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"></path>
              </svg>
            </button>
            <button 
              className="ai-assistant-close" 
              onClick={toggleChat}
              aria-label="Close AI Assistant"
            >
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                <line x1="18" y1="6" x2="6" y2="18"></line>
                <line x1="6" y1="6" x2="18" y2="18"></line>
              </svg>
            </button>
          </div>
        </div>

        <div className="ai-assistant-messages">
          {messages.map((message, index) => (
            <>
              {message.isNewSession && (
                <div className="ai-assistant-session-divider">
                  <span>New Session</span>
                </div>
              )}
              <div 
                key={message.id} 
                className={`ai-assistant-message ${message.isUser ? 'user' : 'ai'}`}
              >
                {!message.isUser && (
                  <div className="ai-assistant-avatar"></div>
                )}
                <div className="ai-assistant-message-bubble">
                  {!message.isUser && message.label && (
                    <div className="ai-assistant-label">{message.label}</div>
                  )}
                  <div className="ai-assistant-message-content">
                    {message.text.split('\n').map((text, i) => (
                      <p key={i}>{text}</p>
                    ))}
                    <span className="ai-assistant-message-time">
                      {formatTime(message.timestamp)}
                    </span>
                  </div>
                  
                  {/* Show rating prompt after the last AI message when a closing statement was detected */}
                  {!message.isUser && 
                   index === messages.length - 1 && 
                   showEndRating && 
                   !conversationRating && (
                    <div className="ai-assistant-end-rating">
                      <div className="ai-assistant-end-rating-prompt">
                        Was this conversation helpful?
                      </div>
                      <div className="ai-assistant-end-rating-buttons">
                        <button 
                          className="ai-assistant-rating-btn thumbs-up"
                          onClick={() => handleRateConversation('thumbsUp')}
                          title="Thumbs Up"
                        >
                          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                            <path d="M7 10v12"></path>
                            <path d="M15 5.88 14 10h5.83a2 2 0 0 1 1.92 2.56l-2.33 8A2 2 0 0 1 17.5 22H4a2 2 0 0 1-2-2v-8a2 2 0 0 1 2-2h2.76a2 2 0 0 0 1.79-1.11L12 2h0a3.13 3.13 0 0 1 3 3.88Z"></path>
                          </svg>
                        </button>
                        <button 
                          className="ai-assistant-rating-btn thumbs-down"
                          onClick={() => handleRateConversation('thumbsDown')}
                          title="Thumbs Down"
                        >
                          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                            <path d="M17 14V2"></path>
                            <path d="M9 18.12 10 14H4.17a2 2 0 0 1-1.92-2.56l2.33-8A2 2 0 0 1 6.5 2H20a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2h-2.76a2 2 0 0 0-1.79 1.11L12 22h0a3.13 3.13 0 0 1-3-3.88Z"></path>
                          </svg>
                        </button>
                      </div>
                    </div>
                  )}
                  
                  {!message.isUser && 
                   index === messages.length - 1 && 
                   conversationRating && (
                    <div className="ai-assistant-feedback-thanks">
                      Thanks for your feedback
                    </div>
                  )}
                </div>
              </div>
            </>
          ))}
          {isOperating && (
            <div className="ai-assistant-message ai">
              <div className="ai-assistant-avatar"></div>
              <div className="ai-assistant-message-bubble">
                <div className="ai-assistant-operating">
                  <span className="ai-assistant-operating-text">Agent operating...</span>
                </div>
              </div>
            </div>
          )}
          {isLoading && !isOperating && (
            <div className="ai-assistant-message ai">
              <div className="ai-assistant-avatar"></div>
              <div className="ai-assistant-message-bubble">
                <div className="ai-assistant-message-content">
                  <div className="ai-assistant-typing-indicator">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        <div className="ai-assistant-footer">
          <div className="ai-assistant-actions">
            <button 
              className="ai-assistant-transfer-button"
              onClick={handleTransferToHuman}
            >
              Connect to Human Agent
            </button>
          </div>
          
          <div className="ai-assistant-input-container">
            <input
              ref={inputRef}
              type="text"
              className="ai-assistant-input"
              placeholder="Type your question..."
              value={inputMessage}
              onChange={handleInputChange}
              onKeyPress={handleKeyPress}
            />
            <button 
              className="ai-assistant-send"
              onClick={sendMessage}
              disabled={!inputMessage.trim() || isLoading}
              aria-label="Send message"
            >
              Send
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AIAssistantWindow; 