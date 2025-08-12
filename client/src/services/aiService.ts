import { api } from './api';

export interface AIMessage {
  id: string;
  text: string;
  isUser: boolean;
  timestamp: Date;
  label?: string; // Optional label property to identify message sender
  isNewSession?: boolean;
}

interface OpenAIMessage {
  role: 'system' | 'user' | 'assistant';
  content: string;
}

interface OpenAIResponse {
  choices: {
    message: {
      content: string;
    };
    index: number;
    finish_reason: string;
  }[];
}

// Fallback mock response function if OpenAI API is not available
const getMockAIResponse = async (message: string): Promise<string> => {
  // Simple response logic, can be extended as needed
  if (message.toLowerCase().includes('hello') || message.toLowerCase().includes('hi')) {
    return 'Hello! I am the CareerMatch AI assistant. I can help you learn about platform features, answer questions, or provide usage suggestions. How can I assist you today?';
  } else if (message.toLowerCase().includes('feature') || message.toLowerCase().includes('use')) {
    return 'CareerMatch platform offers these main features:\n1. Job search and application\n2. Network building and social connections\n3. Professional skills showcase\n4. Recruitment posting (for recruiters)\n\nWhich aspect would you like to know more about?';
  } else if (message.toLowerCase().includes('resume') || message.toLowerCase().includes('profile')) {
    return 'In the "Profile" page, you can upload and edit your resume information. A complete profile significantly increases your job search success rate. Would you like guidance on how to optimize your resume?';
  } else if (message.toLowerCase().includes('recruit') || message.toLowerCase().includes('hire')) {
    return 'As a recruiter, you can create new job postings on the "Post Job" page. The system will match the most suitable candidates based on your requirements. You can also directly search the talent pool for ideal candidates.';
  } else {
    return 'Thank you for your question! I may not fully understand your inquiry right now. Could you try describing more specifically what help you need, or ask me directly about job searching, profiles, networking, or platform features?';
  }
};

// Store conversation history for context
let conversationHistory: OpenAIMessage[] = [
  {
    role: 'system',
    content: 'You are a helpful AI assistant for the CareerMatch platform, a career networking and job search website. Your name is CareerMatch Assistant. Provide concise, helpful answers about career development, job searching, resume building, networking, and using the CareerMatch platform. Be professional, encouraging, and keep responses brief but informative.'
  }
];

// Call OpenAI API
const callOpenAI = async (userMessage: string): Promise<string> => {
  try {
    const apiKey = import.meta.env.VITE_OPENAI_API_KEY;
    const model = import.meta.env.VITE_OPENAI_MODEL || 'gpt-3.5-turbo';
    
    if (!apiKey) {
      console.warn('OpenAI API key not found. Falling back to mock responses.');
      return getMockAIResponse(userMessage);
    }
    
    // Add user message to conversation history
    conversationHistory.push({
      role: 'user',
      content: userMessage
    });
    
    // Limit conversation history to last 10 messages to manage token usage
    if (conversationHistory.length > 11) {
      // Keep the system message and most recent exchanges
      conversationHistory = [
        conversationHistory[0],
        ...conversationHistory.slice(conversationHistory.length - 10)
      ];
    }
    
    const response = await fetch('https://api.openai.com/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${apiKey}`
      },
      body: JSON.stringify({
        model: model,
        messages: conversationHistory,
        max_tokens: 400,
        temperature: 0.7
      })
    });
    
    if (!response.ok) {
      throw new Error(`OpenAI API error: ${response.status} ${response.statusText}`);
    }
    
    const data = await response.json() as OpenAIResponse;
    const assistantResponse = data.choices[0]?.message?.content || 'Sorry, I could not generate a response.';
    
    // Add assistant response to conversation history
    conversationHistory.push({
      role: 'assistant',
      content: assistantResponse
    });
    
    return assistantResponse;
  } catch (error) {
    console.error('Error calling OpenAI:', error);
    return 'Sorry, I encountered a problem connecting to my knowledge base. Let me try a simpler response...';
  }
};

// Function to get AI response - tries OpenAI first, falls back to mock responses
export const getAIResponse = async (message: string): Promise<string> => {
  try {
    // Try to use OpenAI
    return await callOpenAI(message);
  } catch (error) {
    console.error('Failed to get AI response:', error);
    // Fall back to mock responses
    return await getMockAIResponse(message);
  }
};

// Generate unique ID
export const generateId = (): string => {
  return Date.now().toString(36) + Math.random().toString(36).substr(2);
};

// Check if OpenAI integration is working
export const isUsingOpenAI = async (): Promise<boolean> => {
  try {
    // Print environment variables for debugging
    console.log('ENV check - VITE_OPENAI_API_KEY exists:', !!import.meta.env.VITE_OPENAI_API_KEY);
    
    const apiKey = import.meta.env.VITE_OPENAI_API_KEY;
    if (!apiKey) {
      console.warn('OpenAI API key not found in environment variables');
      return false;
    }
    
    // Validate API key format
    if (!apiKey.startsWith('sk-') || apiKey.length < 20) {
      console.warn('OpenAI API key format appears to be invalid');
      return false;
    }
    
    console.log('OpenAI integration appears to be configured correctly');
    return true;
  } catch (error) {
    console.error('Error checking OpenAI status:', error);
    return false;
  }
}; 