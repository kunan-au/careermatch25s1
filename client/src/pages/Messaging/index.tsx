import { useState } from 'react';
import { ChatContact, Message } from '@/types/chat';

// Filter type definition
type FilterType = 'all' | 'connections' | 'unread';

const MOCK_CONTACTS: ChatContact[] = [
  {
    id: 1,
    name: "Henri Rousseau",
    title: "Software Engineer",
    lastMessage: "Hey Julia!",
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
    name: "Kate at LinkedIn",
    title: "LinkedIn Offer",
    lastMessage: "Find the right person for your role",
    timestamp: "Mar 20",
    unread: true,
    isConnection: false
  }
];

export default function MessagingPage() {
  const [selectedContact, setSelectedContact] = useState<ChatContact | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [activeFilter, setActiveFilter] = useState<FilterType>('all');

  // Filter contacts
  const filteredContacts = MOCK_CONTACTS.filter(contact => {
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
                className="p-3 hover:bg-gray-50 cursor-pointer"
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
              <div className="flex-1 p-4">
                {/* 消息列表将在这里 */}
              </div>
              <div className="p-4 border-t">
                <div className="flex gap-2">
                  <input
                    type="text"
                    placeholder="Write a message or attach a file"
                    className="flex-1 px-4 py-2 text-sm border rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
                  />
                  <button className="px-4 py-2 bg-green-500 text-white text-sm rounded-lg hover:bg-green-600">
                    Send
                  </button>
                </div>
              </div>
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