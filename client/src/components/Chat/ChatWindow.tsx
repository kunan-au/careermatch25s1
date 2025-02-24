import { useState } from 'react';
import { ChatComponent } from './ChatComponent';
import './ChatWindow.css';

export function ChatWindow() {
  const [isExpanded, setIsExpanded] = useState(false);

  return (
    <div className={`chat-window ${isExpanded ? 'expanded' : 'collapsed'}`}>
      <div className="chat-header" onClick={() => setIsExpanded(!isExpanded)}>
        <div className="header-content">
          <span>Messaging</span>
          <button className="toggle-button">
            {isExpanded ? '▼' : '▲'}
          </button>
        </div>
      </div>
      {isExpanded && <ChatComponent />}
    </div>
  );
} 