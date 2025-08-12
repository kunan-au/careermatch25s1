import { AIMessage } from './aiService';

export interface ChatSession {
  id: string;
  title: string;
  messages: AIMessage[];
  createdAt: Date;
  updatedAt: Date;
}

export interface MessageFeedback {
  messageId: string;
  rating: 'helpful' | 'unhelpful';
  comment?: string;
}

const HISTORY_STORAGE_KEY = 'ai_chat_history';
const FEEDBACK_STORAGE_KEY = 'ai_feedback';

// Get all chat sessions
export const getAllChatSessions = (): ChatSession[] => {
  try {
    const stored = localStorage.getItem(HISTORY_STORAGE_KEY);
    if (!stored) return [];
    
    const parsed = JSON.parse(stored);
    return parsed.map((session: any) => ({
      ...session,
      createdAt: new Date(session.createdAt),
      updatedAt: new Date(session.updatedAt),
      messages: session.messages.map((msg: any) => ({
        ...msg,
        timestamp: new Date(msg.timestamp)
      }))
    }));
  } catch (error) {
    console.error('Failed to load chat history:', error);
    return [];
  }
};

// Get a specific chat session by ID
export const getChatSession = (sessionId: string): ChatSession | null => {
  const sessions = getAllChatSessions();
  return sessions.find(s => s.id === sessionId) || null;
};

// Create a new chat session
export const createChatSession = (title: string): ChatSession => {
  const id = Date.now().toString(36) + Math.random().toString(36).substr(2);
  const now = new Date();
  
  const newSession: ChatSession = {
    id,
    title,
    messages: [],
    createdAt: now,
    updatedAt: now
  };
  
  const sessions = getAllChatSessions();
  sessions.push(newSession);
  saveChatSessions(sessions);
  
  return newSession;
};

// Update an existing chat session
export const updateChatSession = (
  sessionId: string, 
  updates: {title?: string, messages?: AIMessage[]}
): ChatSession | null => {
  const sessions = getAllChatSessions();
  const sessionIndex = sessions.findIndex(s => s.id === sessionId);
  
  if (sessionIndex === -1) return null;
  
  const updatedSession = {
    ...sessions[sessionIndex],
    ...updates,
    updatedAt: new Date()
  };
  
  sessions[sessionIndex] = updatedSession;
  saveChatSessions(sessions);
  
  return updatedSession;
};

// Delete a chat session
export const deleteChatSession = (sessionId: string): boolean => {
  let sessions = getAllChatSessions();
  const initialLength = sessions.length;
  
  sessions = sessions.filter(s => s.id !== sessionId);
  
  if (sessions.length === initialLength) {
    return false; // Nothing was deleted
  }
  
  saveChatSessions(sessions);
  return true;
};

// Add message to a specific session
export const addMessageToSession = (
  sessionId: string,
  message: AIMessage
): ChatSession | null => {
  const sessions = getAllChatSessions();
  const sessionIndex = sessions.findIndex(s => s.id === sessionId);
  
  if (sessionIndex === -1) return null;
  
  const updatedMessages = [...sessions[sessionIndex].messages, message];
  
  sessions[sessionIndex] = {
    ...sessions[sessionIndex],
    messages: updatedMessages,
    updatedAt: new Date()
  };
  
  saveChatSessions(sessions);
  return sessions[sessionIndex];
};

// Save all chat sessions to localStorage
const saveChatSessions = (sessions: ChatSession[]): void => {
  try {
    localStorage.setItem(HISTORY_STORAGE_KEY, JSON.stringify(sessions));
  } catch (error) {
    console.error('Failed to save chat history:', error);
  }
};

// Clear all chat history
export const clearAllChatHistory = (): void => {
  localStorage.removeItem(HISTORY_STORAGE_KEY);
};

// Store feedback for a message
export const saveFeedback = (feedback: MessageFeedback): void => {
  try {
    const stored = localStorage.getItem(FEEDBACK_STORAGE_KEY);
    const feedbacks = stored ? JSON.parse(stored) : [];
    
    // Check if feedback for this message already exists
    const existingIndex = feedbacks.findIndex(
      (f: MessageFeedback) => f.messageId === feedback.messageId
    );
    
    if (existingIndex !== -1) {
      feedbacks[existingIndex] = feedback;
    } else {
      feedbacks.push(feedback);
    }
    
    localStorage.setItem(FEEDBACK_STORAGE_KEY, JSON.stringify(feedbacks));
  } catch (error) {
    console.error('Failed to save feedback:', error);
  }
};

// Get feedback for a specific message
export const getFeedback = (messageId: string): MessageFeedback | null => {
  try {
    const stored = localStorage.getItem(FEEDBACK_STORAGE_KEY);
    if (!stored) return null;
    
    const feedbacks = JSON.parse(stored);
    return feedbacks.find((f: MessageFeedback) => f.messageId === messageId) || null;
  } catch (error) {
    console.error('Failed to get feedback:', error);
    return null;
  }
}; 