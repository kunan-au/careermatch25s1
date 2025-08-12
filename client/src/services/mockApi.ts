import { ChatContact, Message } from '@/types/chat';

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

export const mockApi = {
  getContacts: () => {
    return Promise.resolve({
      data: MOCK_CONTACTS
    });
  },
  
  getMessages: (contactId: number) => {
    return Promise.resolve({
      data: [
        {
          id: 1,
          text: "Hey Julia!",
          sender: "Henri Rousseau",
          timestamp: "8:55 AM",
        }
      ]
    });
  }
}; 