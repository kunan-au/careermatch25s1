import { useState, useEffect } from 'react';
import { api } from '@/services/api';
import { Message } from '@/types/chat';

export function ChatComponent() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [newMessage, setNewMessage] = useState('');

  useEffect(() => {
    // 获取消息列表
    api.getMessages().then(response => {
      setMessages(response.data);
    });
  }, []);

  const handleSend = async () => {
    if (!newMessage.trim()) return;
    
    const response = await api.sendMessage(newMessage);
    setMessages(prev => [...prev, response.data]);
    setNewMessage('');
  };

  return (
    <div>
      {/* 聊天界面 UI */}
      <div className="messages">
        {messages.map(msg => (
          <div key={msg.id} className="message">
            <span className="sender">{msg.sender}: </span>
            <span className="text">{msg.text}</span>
            <span className="timestamp">{new Date(msg.timestamp).toLocaleTimeString()}</span>
          </div>
        ))}
      </div>
      <div className="input-area">
        <input
          value={newMessage}
          onChange={e => setNewMessage(e.target.value)}
          placeholder="Type a message..."
        />
        <button onClick={handleSend}>Send</button>
      </div>
    </div>
  );
} 