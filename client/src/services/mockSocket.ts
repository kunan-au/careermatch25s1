import { Message } from '@/types/chat';
import { socketService, SocketEvent } from './socket';

// Mock user data
const MOCK_USERS = [
  { id: 1, name: 'Henri Rousseau', isOnline: true },
  { id: 2, name: 'Justice Moore', isOnline: false },
  { id: 3, name: 'Kate at LinkedIn', isOnline: true },
];

// Mock message data
const MOCK_MESSAGES: Message[] = [
  {
    id: 1,
    text: 'Hey Julia!',
    sender: 'Henri Rousseau',
    timestamp: new Date(Date.now() - 3600000).toISOString(), // 1 hour ago
  },
  {
    id: 2,
    text: 'Hi Henri, how are you?',
    sender: 'Me',
    timestamp: new Date(Date.now() - 3500000).toISOString(),
  },
  {
    id: 3,
    text: 'I\'m doing great! Just wanted to check in about the project.',
    sender: 'Henri Rousseau',
    timestamp: new Date(Date.now() - 3400000).toISOString(),
  },
];

// Mock WebSocket service
class MockSocketService {
  private static instance: MockSocketService;
  private isConnected = false;
  private currentUserId: number | null = null;
  private messageId = MOCK_MESSAGES.length + 1;
  private lastRespondedUsers: Set<string> = new Set(); // Track users who have already responded

  private constructor() {}

  public static getInstance(): MockSocketService {
    if (!MockSocketService.instance) {
      MockSocketService.instance = new MockSocketService();
    }
    return MockSocketService.instance;
  }

  // Initialize mock service
  public init(): void {
    // Simulate user login
    this.currentUserId = 0; // Current user ID
    this.isConnected = true;
    this.lastRespondedUsers.clear(); // Clear the list of users who have responded

    // Add message listener
    socketService.addMessageListener(this.handleIncomingMessage);

    // Send initial messages
    setTimeout(() => {
      // Only send initial messages once, don't repeat
      const sentMessageIds = new Set();
      MOCK_MESSAGES.forEach(message => {
        if (!sentMessageIds.has(message.id)) {
          socketService['messageListeners'].forEach(listener => listener(message));
          sentMessageIds.add(message.id);
        }
      });
    }, 1000);

    // Simulate user online status updates
    setInterval(() => {
      const randomUser = MOCK_USERS[Math.floor(Math.random() * MOCK_USERS.length)];
      const newStatus = { userId: randomUser.id, isOnline: Math.random() > 0.3 };
      
      socketService['statusListeners'].forEach(listener => listener(newStatus));
    }, 30000); // Update every 30 seconds
  }

  // Handle outgoing messages
  private handleIncomingMessage = (message: Message): void => {
    if (message.sender === 'Me') {
      // Simulate response, but ensure each user only responds once
      setTimeout(() => {
        // Randomly select a user, but avoid duplicate responses
        let availableUsers = MOCK_USERS.filter(user => !this.lastRespondedUsers.has(user.name));
        
        // If all users have responded, reset
        if (availableUsers.length === 0) {
          this.lastRespondedUsers.clear();
          availableUsers = MOCK_USERS;
        }
        
        const randomUser = availableUsers[Math.floor(Math.random() * availableUsers.length)];
        this.lastRespondedUsers.add(randomUser.name); // Mark this user as having responded
        
        let reply: Message;
        
        // Handle different message types
        if (message.type === 'audio') {
          // Reply to voice message
          reply = {
            id: this.messageId++,
            text: "I received your voice message. Thanks!",
            sender: randomUser.name,
            timestamp: new Date().toISOString(),
            type: 'text'
          };
        } else if (message.type === 'file') {
          // Reply to file message
          reply = {
            id: this.messageId++,
            text: `Thanks for sharing the file${message.fileName ? ': ' + message.fileName : ''}. I'll take a look at it.`,
            sender: randomUser.name,
            timestamp: new Date().toISOString(),
            type: 'text'
          };
        } else {
          // Reply to text message
          reply = {
            id: this.messageId++,
            text: this.getRandomReply(),
            sender: randomUser.name,
            timestamp: new Date().toISOString(),
            type: 'text'
          };
        }
        
        socketService['messageListeners'].forEach(listener => listener(reply));
      }, 1000 + Math.random() * 2000); // Reply after 1-3 seconds
    }
  };

  // Get random reply
  private getRandomReply(): string {
    const replies = [
      'That sounds great!',
      'I\'ll get back to you on that.',
      'Can we discuss this further?',
      'Thanks for letting me know.',
      'I appreciate your input.',
      'Let\'s schedule a meeting to discuss this.',
      'I\'m not sure I understand. Can you clarify?',
      'I agree with your approach.',
      'I have some concerns about this.',
      'Let\'s move forward with this plan.',
    ];
    
    return replies[Math.floor(Math.random() * replies.length)];
  }
}

export const mockSocketService = MockSocketService.getInstance(); 