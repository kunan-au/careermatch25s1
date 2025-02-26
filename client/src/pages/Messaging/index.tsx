import { useState, useEffect, useRef } from 'react';
import { ChatContact, Message } from '@/types/chat';
import { socketService } from '@/services/socket';
import { mockSocketService } from '@/services/mockSocket';
import VoiceRecorder from '@/components/VoiceRecorder';
import VoiceMessage from '@/components/VoiceMessage';
import FileMessage from '@/components/FileMessage';

// Filter type definition
type FilterType = 'all' | 'connections' | 'unread';

// Mock contact data
const MOCK_CONTACTS: ChatContact[] = [
  {
    id: 1,
    name: "Henri Rousseau",
    title: "Software Engineer",
    lastMessage: "Here's the proposal document we discussed.",
    timestamp: "8:55 AM",
    isOnline: true,
    unread: true,
    isConnection: true
  },
  {
    id: 2,
    name: "Justice Moore",
    lastMessage: "It's my pleasure",
    timestamp: "Mar 26",
    unread: false,
    isConnection: true
  },
  {
    id: 3,
    name: "Kate at CareerMatch",
    title: "LinkedIn Offer",
    lastMessage: "Find the right person for your role",
    timestamp: "Mar 20",
    unread: true,
    isConnection: false
  }
];

// Mock message data for each contact
const MOCK_CONTACT_MESSAGES: Record<number, Message[]> = {
  1: [
    {
      id: 101,
      text: "Hey Julia!",
      sender: "Henri Rousseau",
      timestamp: new Date(Date.now() - 3600000).toISOString(),
      type: 'text'
    },
    {
      id: 102,
      text: "Hi Henri, how are you?",
      sender: "Me",
      timestamp: new Date(Date.now() - 3500000).toISOString(),
      type: 'text'
    },
    {
      id: 103,
      text: "I'm doing great! Just wanted to check in about the project.",
      sender: "Henri Rousseau",
      timestamp: new Date(Date.now() - 3400000).toISOString(),
      type: 'text'
    },
    {
      id: 104,
      text: "I've been working on the design mockups.",
      sender: "Me",
      timestamp: new Date(Date.now() - 3300000).toISOString(),
      type: 'text'
    },
    {
      id: 105,
      fileName: "project_proposal.pdf",
      fileUrl: "#",
      sender: "Henri Rousseau",
      timestamp: new Date(Date.now() - 3200000).toISOString(),
      type: 'file'
    },
    {
      id: 106,
      text: "Here's the proposal document we discussed.",
      sender: "Henri Rousseau",
      timestamp: new Date(Date.now() - 3190000).toISOString(),
      type: 'text'
    }
  ],
  2: [
    {
      id: 201,
      text: "Thanks for your help yesterday",
      sender: "Justice Moore",
      timestamp: new Date(Date.now() - 86400000).toISOString(),
      type: 'text'
    },
    {
      id: 202,
      text: "It's my pleasure",
      sender: "Me",
      timestamp: new Date(Date.now() - 86000000).toISOString(),
      type: 'text'
    },
    {
      id: 203,
      text: "That sounds great!",
      sender: "Justice Moore",
      timestamp: new Date(Date.now() - 3600000).toISOString(),
      type: 'text'
    }
  ],
  3: [
    {
      id: 301,
      text: "Find the right person for your role",
      sender: "Kate at CareerMatch",
      timestamp: new Date(Date.now() - 172800000).toISOString(),
      type: 'text'
    },
    {
      id: 302,
      text: "I'm not sure I understand. Can you clarify?",
      sender: "Kate at CareerMatch",
      timestamp: new Date(Date.now() - 3600000).toISOString(),
      type: 'text'
    },
    {
      id: 303,
      text: "Let's schedule a meeting to discuss this.",
      sender: "Kate at CareerMatch",
      timestamp: new Date(Date.now() - 1800000).toISOString(),
      type: 'text'
    },
    {
      id: 304,
      text: "Thanks for letting me know.",
      sender: "Kate at CareerMatch",
      timestamp: new Date(Date.now() - 600000).toISOString(),
      type: 'text'
    }
  ]
};

// Create a function to get the last message for a contact
const getLastMessageInfo = (messages: Message[]) => {
  if (!messages || messages.length === 0) return { text: '', timestamp: '' };
  
  const lastMsg = messages[messages.length - 1];
  let text = '';
  
  if (lastMsg.type === 'audio') {
    text = 'Voice message';
  } else if (lastMsg.type === 'file' && lastMsg.fileName) {
    text = `File: ${lastMsg.fileName}`;
  } else if (lastMsg.text) {
    text = lastMsg.text;
  }
  
  return { 
    text, 
    timestamp: lastMsg.timestamp 
  };
};

// Format timestamp
const formatTimestamp = (timestamp: string): string => {
  const date = new Date(timestamp);
  const now = new Date();
  const diffDays = Math.floor((now.getTime() - date.getTime()) / (1000 * 60 * 60 * 24));
  
  if (diffDays === 0) {
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  } else if (diffDays < 7) {
    const days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
    return days[date.getDay()];
  } else {
    return `${date.getMonth() + 1}/${date.getDate()}`;
  }
};

// Create initial contact data, ensuring last message matches message history
const createInitialContacts = () => {
  return MOCK_CONTACTS.map(contact => {
    const messages = MOCK_CONTACT_MESSAGES[contact.id] || [];
    const { text, timestamp } = getLastMessageInfo(messages);
    
    return {
      ...contact,
      lastMessage: text || contact.lastMessage,
      timestamp: timestamp ? formatTimestamp(timestamp) : contact.timestamp
    };
  });
};

export default function MessagingPage() {
  const [selectedContact, setSelectedContact] = useState<ChatContact | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [activeFilter, setActiveFilter] = useState<FilterType>('all');
  const [messages, setMessages] = useState<Message[]>([]);
  const [newMessage, setNewMessage] = useState('');
  const [contacts, setContacts] = useState<ChatContact[]>([]);
  const [showVoiceRecorder, setShowVoiceRecorder] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const [contactMessages, setContactMessages] = useState<Record<number, Message[]>>(MOCK_CONTACT_MESSAGES);
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Initialize contact list
  useEffect(() => {
    setContacts(createInitialContacts());
  }, []);

  // Initialize WebSocket connection
  useEffect(() => {
    // Use mock service in development environment
    mockSocketService.init();

    // Add message listeners
    socketService.addMessageListener(handleNewMessage);
    socketService.addStatusListener(handleStatusChange);

    return () => {
      // Clean up listeners
      socketService.removeMessageListener(handleNewMessage);
      socketService.removeStatusListener(handleStatusChange);
    };
  }, []);

  // Handle new messages
  const handleNewMessage = (message: Message) => {
    // Find which contact this message belongs to
    const contactId = contacts.find(c => c.name === message.sender)?.id || 
                     (selectedContact ? selectedContact.id : null);
    
    if (contactId) {
      // Update contact messages store for this contact
      setContactMessages(prev => {
        // Check if message already exists
        const existingMessages = prev[contactId] || [];
        const messageExists = existingMessages.some(msg => msg.id === message.id);
        
        // If message already exists, don't add it
        if (messageExists) {
          return prev;
        }
        
        const updatedMessages = {
          ...prev,
          [contactId]: [...existingMessages, message]
        };
        
        // If this is the currently selected contact, also update current message list
        if (selectedContact && selectedContact.id === contactId) {
          // Ensure we don't add duplicate messages
          setMessages(prev => {
            const messageExists = prev.some(msg => msg.id === message.id);
            return messageExists ? prev : [...prev, message];
          });
        }
        
        return updatedMessages;
      });
      
      // Update contact list with last message
      setContacts(prev => 
        prev.map(contact => {
          if (contact.id === contactId) {
            let lastMessageText = '';
            
            // Format last message based on type
            if (message.type === 'audio') {
              lastMessageText = 'Voice message';
            } else if (message.type === 'file' && message.fileName) {
              lastMessageText = `File: ${message.fileName}`;
            } else if (message.text) {
              lastMessageText = message.text;
            }
            
            return { 
              ...contact, 
              lastMessage: lastMessageText, 
              timestamp: formatTimestamp(message.timestamp),
              unread: selectedContact?.id !== contact.id
            };
          }
          return contact;
        })
      );
    }
  };

  // Handle online status changes
  const handleStatusChange = (status: { userId: number; isOnline: boolean }) => {
    setContacts(prev => 
      prev.map(contact => 
        contact.id === status.userId 
          ? { ...contact, isOnline: status.isOnline } 
          : contact
      )
    );
  };

  // Load contact message history when selecting a contact
  useEffect(() => {
    if (selectedContact) {
      // Load messages for the selected contact
      const contactId = selectedContact.id;
      
      // Ensure messages aren't duplicated, use Set to filter duplicate message IDs
      const uniqueMessages = contactMessages[contactId] || [];
      const messageIds = new Set();
      const filteredMessages = uniqueMessages.filter(msg => {
        if (messageIds.has(msg.id)) {
          return false;
        }
        messageIds.add(msg.id);
        return true;
      });
      
      setMessages(filteredMessages);
      
      // Mark as read
      setContacts(prev => 
        prev.map(contact => 
          contact.id === selectedContact.id 
            ? { ...contact, unread: false } 
            : contact
        )
      );
    }
  }, [selectedContact, contactMessages]);

  // Scroll to latest message
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Send text message
  const sendTextMessage = () => {
    if (!newMessage.trim() || !selectedContact) return;

    const message: Message = {
      id: Date.now(),
      text: newMessage,
      sender: 'Me',
      timestamp: new Date().toISOString(),
      type: 'text'
    };

    // Send message to WebSocket server
    socketService.sendMessage({
      text: newMessage,
      sender: 'Me',
      type: 'text'
    });

    // Update contact messages store
    setContactMessages(prev => {
      const contactId = selectedContact.id;
      const existingMessages = prev[contactId] || [];
      
      // Check if message already exists (based on ID)
      const messageExists = existingMessages.some(msg => msg.id === message.id);
      if (messageExists) {
        return prev;
      }
      
      const updatedMessages = {
        ...prev,
        [contactId]: [...existingMessages, message]
      };
      
      // Update current message list
      setMessages(prev => {
        const messageExists = prev.some(msg => msg.id === message.id);
        return messageExists ? prev : [...prev, message];
      });
      
      return updatedMessages;
    });
    
    // Update contact list with last message
    setContacts(prev => 
      prev.map(contact => 
        contact.id === selectedContact.id 
          ? { 
              ...contact, 
              lastMessage: newMessage, 
              timestamp: formatTimestamp(new Date().toISOString()) 
            } 
          : contact
      )
    );

    // Clear input field
    setNewMessage('');
  };

  // Handle voice recording completion
  const handleVoiceRecordingComplete = (audioBlob: Blob) => {
    if (!selectedContact) return;
    
    // Create audio URL
    const audioUrl = URL.createObjectURL(audioBlob);
    
    // Create voice message
    const message: Message = {
      id: Date.now(),
      sender: 'Me',
      timestamp: new Date().toISOString(),
      audioUrl,
      type: 'audio'
    };
    
    // Update contact messages store
    setContactMessages(prev => {
      const contactId = selectedContact.id;
      const existingMessages = prev[contactId] || [];
      
      // Check if message already exists (based on ID)
      const messageExists = existingMessages.some(msg => msg.id === message.id);
      if (messageExists) {
        return prev;
      }
      
      const updatedMessages = {
        ...prev,
        [contactId]: [...existingMessages, message]
      };
      
      // Update current message list
      setMessages(prev => {
        const messageExists = prev.some(msg => msg.id === message.id);
        return messageExists ? prev : [...prev, message];
      });
      
      return updatedMessages;
    });
    
    // Update contact list with last message
    setContacts(prev => 
      prev.map(contact => 
        contact.id === selectedContact.id 
          ? { 
              ...contact, 
              lastMessage: 'Voice message', 
              timestamp: formatTimestamp(new Date().toISOString()) 
            } 
          : contact
      )
    );
    
    // Hide recording component
    setShowVoiceRecorder(false);
  };

  // Handle file upload
  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (!event.target.files || !event.target.files.length || !selectedContact) return;
    
    const file = event.target.files[0];
    const fileUrl = URL.createObjectURL(file);
    
    // Create file message
    const message: Message = {
      id: Date.now(),
      sender: 'Me',
      timestamp: new Date().toISOString(),
      fileUrl,
      fileName: file.name,
      type: 'file'
    };
    
    // Send file message to WebSocket server
    // In a real implementation, this would upload the file to a server
    socketService.sendFileMessage(file, file.name, 'file');
    
    // Update contact messages store
    setContactMessages(prev => {
      const contactId = selectedContact.id;
      const existingMessages = prev[contactId] || [];
      
      // Check if message already exists (based on ID)
      const messageExists = existingMessages.some(msg => msg.id === message.id);
      if (messageExists) {
        return prev;
      }
      
      const updatedMessages = {
        ...prev,
        [contactId]: [...existingMessages, message]
      };
      
      // Update current message list
      setMessages(prev => {
        const messageExists = prev.some(msg => msg.id === message.id);
        return messageExists ? prev : [...prev, message];
      });
      
      return updatedMessages;
    });
    
    // Update contact list with last message
    setContacts(prev => 
      prev.map(contact => 
        contact.id === selectedContact.id 
          ? { 
              ...contact, 
              lastMessage: `File: ${file.name}`, 
              timestamp: formatTimestamp(new Date().toISOString()) 
            } 
          : contact
      )
    );
    
    // Clear the file input
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  // Trigger file input click
  const openFileDialog = () => {
    fileInputRef.current?.click();
  };

  // Filter contacts
  const filteredContacts = contacts.filter(contact => {
    // Search filter
    const matchesSearch = contact.name.toLowerCase().includes(searchTerm.toLowerCase());
    
    // Type filter
    const matchesFilter = 
      activeFilter === 'all' ? true :
      activeFilter === 'connections' ? contact.isConnection :
      activeFilter === 'unread' ? contact.unread :
      true;

    return matchesSearch && matchesFilter;
  });

  // Render message content
  const renderMessageContent = (message: Message) => {
    if (message.type === 'audio' && message.audioUrl) {
      return (
        <VoiceMessage 
          audioUrl={message.audioUrl} 
          timestamp={message.timestamp} 
          sender={message.sender}
          formatTimestamp={formatTimestamp}
        />
      );
    } else if (message.type === 'file' && message.fileUrl && message.fileName) {
      return (
        <FileMessage
          fileUrl={message.fileUrl}
          fileName={message.fileName}
          timestamp={message.timestamp}
          sender={message.sender}
          formatTimestamp={formatTimestamp}
        />
      );
    } else {
      return (
        <>
          <p className="text-sm">{message.text}</p>
          <p className="text-xs mt-1 opacity-70">
            {formatTimestamp(message.timestamp)}
          </p>
        </>
      );
    }
  };

  return (
    <div className="max-w-6xl mx-auto p-4">
      <div className="flex h-[calc(100vh-100px)] bg-white rounded-lg shadow-lg">
        {/* Left sidebar - Contact list */}
        <div className="w-1/3 border-r">
          {/* Search box */}
          <div className="p-4 border-b">
            <div className="relative">
              <input
                type="text"
                placeholder="Search messages"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-10 pr-4 py-2 border rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-green-500"
              />
              <svg
                className="absolute left-3 top-2.5 h-5 w-5 text-gray-400"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
                />
              </svg>
            </div>
          </div>

          {/* Filter options */}
          <div className="p-2 border-b">
            <div className="flex flex-col space-y-1">
              <button
                onClick={() => setActiveFilter('all')}
                className={`text-left px-3 py-2 rounded-lg text-sm ${
                  activeFilter === 'all' ? 'bg-green-50 text-green-600' : 'hover:bg-gray-100'
                }`}
              >
                All Messages
              </button>
              <button
                onClick={() => setActiveFilter('connections')}
                className={`text-left px-3 py-2 rounded-lg text-sm ${
                  activeFilter === 'connections' ? 'bg-green-50 text-green-600' : 'hover:bg-gray-100'
                }`}
              >
                My Connections
              </button>
              <button
                onClick={() => setActiveFilter('unread')}
                className={`text-left px-3 py-2 rounded-lg text-sm ${
                  activeFilter === 'unread' ? 'bg-green-50 text-green-600' : 'hover:bg-gray-100'
                }`}
              >
                Unread
              </button>
            </div>
          </div>

          {/* Contact list */}
          <div className="overflow-y-auto">
            {filteredContacts.map(contact => (
              <div
                key={contact.id}
                className={`p-3 hover:bg-gray-50 cursor-pointer ${
                  selectedContact?.id === contact.id ? 'bg-gray-100' : ''
                }`}
                onClick={() => setSelectedContact(contact)}
              >
                <div className="flex items-start gap-3">
                  <div className="relative">
                    <div className="w-10 h-10 rounded-full bg-gray-200" />
                    {contact.isOnline && (
                      <div className="absolute bottom-0 right-0 w-2 h-2 bg-green-500 rounded-full border-2 border-white" />
                    )}
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex justify-between items-center">
                      <h3 className="font-medium text-sm truncate">
                        {contact.name}
                        {contact.unread && (
                          <span className="ml-2 w-2 h-2 bg-green-500 rounded-full inline-block" />
                        )}
                      </h3>
                      <span className="text-xs text-gray-500 flex-shrink-0">{contact.timestamp}</span>
                    </div>
                    {contact.title && (
                      <p className="text-xs text-gray-500 truncate">{contact.title}</p>
                    )}
                    <p className="text-sm text-gray-600 truncate">{contact.lastMessage}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Right side - Chat area */}
        <div className="flex-1">
          {selectedContact ? (
            <div className="h-full flex flex-col">
              <div className="p-4 border-b">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-full bg-gray-200" />
                  <div>
                    <h2 className="font-medium text-sm">{selectedContact.name}</h2>
                    {selectedContact.title && (
                      <p className="text-xs text-gray-500">{selectedContact.title}</p>
                    )}
                  </div>
                </div>
              </div>
              
              {/* Message list */}
              <div className="flex-1 p-4 overflow-y-auto">
                <div className="space-y-4">
                  {messages.map((message) => (
                    <div 
                      key={message.id} 
                      className={`flex ${message.sender === 'Me' ? 'justify-end' : 'justify-start'}`}
                    >
                      {message.sender !== 'Me' && (
                        <div className="w-8 h-8 rounded-full bg-gray-200 mr-2 flex-shrink-0" />
                      )}
                      <div 
                        className={`max-w-[70%] px-4 py-2 rounded-lg ${
                          message.sender === 'Me' 
                            ? 'bg-green-500 text-white' 
                            : 'bg-gray-100 text-gray-800'
                        }`}
                      >
                        {renderMessageContent(message)}
                      </div>
                      {message.sender === 'Me' && (
                        <div className="w-8 h-8 rounded-full bg-gray-200 ml-2 flex-shrink-0" />
                      )}
                    </div>
                  ))}
                  <div ref={messagesEndRef} />
                </div>
              </div>
              
              {/* Voice recorder component */}
              {showVoiceRecorder && (
                <div className="p-4 border-t">
                  <VoiceRecorder onRecordingComplete={handleVoiceRecordingComplete} />
                </div>
              )}
              
              {/* Input area */}
              {!showVoiceRecorder && (
                <div className="p-4 border-t">
                  <div className="flex gap-2">
                    <input
                      type="text"
                      placeholder="Write a message or attach a file"
                      value={newMessage}
                      onChange={(e) => setNewMessage(e.target.value)}
                      onKeyDown={(e) => e.key === 'Enter' && sendTextMessage()}
                      className="flex-1 px-4 py-2 text-sm border rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
                    />
                    
                    {/* Hidden file input */}
                    <input
                      type="file"
                      ref={fileInputRef}
                      onChange={handleFileUpload}
                      className="hidden"
                    />
                    
                    {/* File button */}
                    <button
                      onClick={openFileDialog}
                      className="p-2 rounded-lg bg-gray-100 text-gray-600 hover:bg-gray-200 focus:outline-none"
                      title="Attach file"
                    >
                      <span className="text-lg">📎</span>
                    </button>
                    
                    {/* Voice button */}
                    <button
                      onClick={() => setShowVoiceRecorder(true)}
                      className="p-2 rounded-lg bg-gray-100 text-gray-600 hover:bg-gray-200 focus:outline-none"
                      title="Record voice message"
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                        <path fillRule="evenodd" d="M7 4a3 3 0 016 0v4a3 3 0 11-6 0V4zm4 10.93A7.001 7.001 0 0017 8a1 1 0 10-2 0A5 5 0 015 8a1 1 0 00-2 0 7.001 7.001 0 006 6.93V17H6a1 1 0 100 2h8a1 1 0 100-2h-3v-2.07z" clipRule="evenodd" />
                      </svg>
                    </button>
                    
                    {/* Send button */}
                    <button 
                      onClick={sendTextMessage}
                      className="px-4 py-2 bg-green-500 text-white text-sm rounded-lg hover:bg-green-600"
                    >
                      Send
                    </button>
                  </div>
                </div>
              )}
            </div>
          ) : (
            <div className="h-full flex items-center justify-center text-gray-500 text-sm">
              Select a conversation to start messaging
            </div>
          )}
        </div>
      </div>
    </div>
  );
} 