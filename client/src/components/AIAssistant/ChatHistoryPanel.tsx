import { useState, useEffect } from 'react';
import { 
  getAllChatSessions, 
  deleteChatSession, 
  ChatSession, 
  createChatSession 
} from '@/services/chatHistoryService';
import styles from './ChatHistoryPanel.module.css';

interface ChatHistoryPanelProps {
  onSelectSession: (sessionId: string) => void;
  onNewChat: () => void;
  currentSessionId?: string;
}

const ChatHistoryPanel = ({ onSelectSession, onNewChat, currentSessionId }: ChatHistoryPanelProps) => {
  const [sessions, setSessions] = useState<ChatSession[]>([]);
  const [isExpanded, setIsExpanded] = useState(false);

  // Load chat sessions on initial render
  useEffect(() => {
    const loadSessions = () => {
      const allSessions = getAllChatSessions();
      // Sort by most recent first
      setSessions(allSessions.sort((a, b) => b.updatedAt.getTime() - a.updatedAt.getTime()));
    };
    
    loadSessions();
    
    // Set up event listener for storage changes from other tabs
    const handleStorageChange = (e: StorageEvent) => {
      if (e.key === 'ai_chat_history') {
        loadSessions();
      }
    };
    
    window.addEventListener('storage', handleStorageChange);
    return () => window.removeEventListener('storage', handleStorageChange);
  }, []);
  
  // Format date as "Mon Day, Year"
  const formatDate = (date: Date) => {
    return new Intl.DateTimeFormat('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric'
    }).format(date);
  };
  
  const handleDeleteSession = (e: React.MouseEvent, sessionId: string) => {
    e.stopPropagation();
    if (window.confirm('Are you sure you want to delete this conversation?')) {
      deleteChatSession(sessionId);
      setSessions(prev => prev.filter(s => s.id !== sessionId));
      
      // If the current session was deleted, create a new one
      if (currentSessionId === sessionId) {
        onNewChat();
      }
    }
  };
  
  // Group sessions by date
  const groupedSessions: { [key: string]: ChatSession[] } = sessions.reduce((groups, session) => {
    const dateKey = formatDate(session.createdAt);
    if (!groups[dateKey]) {
      groups[dateKey] = [];
    }
    groups[dateKey].push(session);
    return groups;
  }, {} as { [key: string]: ChatSession[] });
  
  return (
    <div className={`${styles.panel} ${isExpanded ? styles.expanded : ''}`}>
      <div className={styles.toggleBtn} onClick={() => setIsExpanded(!isExpanded)}>
        {isExpanded ? '◀' : '▶'}
      </div>
      
      <div className={styles.content}>
        <button className={styles.newChatBtn} onClick={onNewChat}>
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M12 5v14M5 12h14" />
          </svg>
          New Chat
        </button>
        
        <div className={styles.sessionList}>
          {Object.keys(groupedSessions).length > 0 ? (
            Object.entries(groupedSessions).map(([date, dateSessions]) => (
              <div key={date} className={styles.dateGroup}>
                <div className={styles.dateHeading}>{date}</div>
                {dateSessions.map(session => (
                  <div 
                    key={session.id} 
                    className={`${styles.sessionItem} ${currentSessionId === session.id ? styles.active : ''}`}
                    onClick={() => onSelectSession(session.id)}
                  >
                    <div className={styles.sessionTitle}>
                      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                        <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
                      </svg>
                      {session.title || 'Untitled Chat'}
                    </div>
                    <button 
                      className={styles.deleteBtn}
                      onClick={(e) => handleDeleteSession(e, session.id)}
                      aria-label="Delete chat"
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                        <path d="M3 6h18M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2M10 11v6M14 11v6" />
                      </svg>
                    </button>
                  </div>
                ))}
              </div>
            ))
          ) : (
            <div className={styles.emptyState}>No conversation history yet</div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ChatHistoryPanel; 