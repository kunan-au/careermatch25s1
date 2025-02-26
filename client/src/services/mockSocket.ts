import { Message } from '@/types/chat';
import { socketService, SocketEvent } from './socket';

// 模拟用户数据
const MOCK_USERS = [
  { id: 1, name: 'Henri Rousseau', isOnline: true },
  { id: 2, name: 'Justice Moore', isOnline: false },
  { id: 3, name: 'Kate at LinkedIn', isOnline: true },
];

// 模拟消息数据
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

// 模拟 WebSocket 服务
class MockSocketService {
  private static instance: MockSocketService;
  private isConnected = false;
  private currentUserId: number | null = null;
  private messageId = MOCK_MESSAGES.length + 1;

  private constructor() {}

  public static getInstance(): MockSocketService {
    if (!MockSocketService.instance) {
      MockSocketService.instance = new MockSocketService();
    }
    return MockSocketService.instance;
  }

  // 初始化模拟服务
  public init(): void {
    // 模拟用户登录
    this.currentUserId = 0; // 当前用户 ID
    this.isConnected = true;

    // 添加消息监听器
    socketService.addMessageListener(this.handleIncomingMessage);

    // 发送初始消息
    setTimeout(() => {
      MOCK_MESSAGES.forEach(message => {
        socketService['messageListeners'].forEach(listener => listener(message));
      });
    }, 1000);

    // 模拟用户在线状态更新
    setInterval(() => {
      const randomUser = MOCK_USERS[Math.floor(Math.random() * MOCK_USERS.length)];
      const newStatus = { userId: randomUser.id, isOnline: Math.random() > 0.3 };
      
      socketService['statusListeners'].forEach(listener => listener(newStatus));
    }, 30000); // 每 30 秒更新一次
  }

  // 处理发出的消息
  private handleIncomingMessage = (message: Message): void => {
    if (message.sender === 'Me') {
      // 模拟对方回复
      setTimeout(() => {
        const randomUser = MOCK_USERS[Math.floor(Math.random() * MOCK_USERS.length)];
        const reply: Message = {
          id: this.messageId++,
          text: this.getRandomReply(),
          sender: randomUser.name,
          timestamp: new Date().toISOString(),
        };
        
        socketService['messageListeners'].forEach(listener => listener(reply));
      }, 1000 + Math.random() * 2000); // 1-3 秒后回复
    }
  };

  // 获取随机回复
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