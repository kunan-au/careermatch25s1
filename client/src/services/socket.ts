import { io, Socket } from 'socket.io-client';
import { Message } from '@/types/chat';

// 定义事件类型
export enum SocketEvent {
  CONNECT = 'connect',
  DISCONNECT = 'disconnect',
  MESSAGE = 'message',
  TYPING = 'typing',
  ONLINE_STATUS = 'online_status',
}

// 单例模式实现 Socket 服务
class SocketService {
  private static instance: SocketService;
  private socket: Socket | null = null;
  private messageListeners: ((message: Message) => void)[] = [];
  private statusListeners: ((status: { userId: number; isOnline: boolean }) => void)[] = [];

  private constructor() {}

  public static getInstance(): SocketService {
    if (!SocketService.instance) {
      SocketService.instance = new SocketService();
    }
    return SocketService.instance;
  }

  // 连接到 WebSocket 服务器
  public connect(userId: number): void {
    // 暂时使用本地 WebSocket 服务
    // 未来可以替换为实际的后端 WebSocket 地址
    this.socket = io('http://localhost:8000', {
      query: { userId: userId.toString() },
    });

    // 设置事件监听器
    this.socket.on(SocketEvent.CONNECT, () => {
      console.log('Connected to WebSocket server');
    });

    this.socket.on(SocketEvent.DISCONNECT, () => {
      console.log('Disconnected from WebSocket server');
    });

    this.socket.on(SocketEvent.MESSAGE, (message: Message) => {
      this.messageListeners.forEach(listener => listener(message));
    });

    this.socket.on(SocketEvent.ONLINE_STATUS, (status: { userId: number; isOnline: boolean }) => {
      this.statusListeners.forEach(listener => listener(status));
    });
  }

  // 断开连接
  public disconnect(): void {
    if (this.socket) {
      this.socket.disconnect();
      this.socket = null;
    }
  }

  // 发送消息
  public sendMessage(message: Omit<Message, 'id' | 'timestamp'>): void {
    if (this.socket) {
      this.socket.emit(SocketEvent.MESSAGE, message);
    } else {
      console.error('Socket not connected');
    }
  }

  // 发送正在输入状态
  public sendTyping(isTyping: boolean, recipientId: number): void {
    if (this.socket) {
      this.socket.emit(SocketEvent.TYPING, { isTyping, recipientId });
    }
  }

  // 添加消息监听器
  public addMessageListener(listener: (message: Message) => void): void {
    this.messageListeners.push(listener);
  }

  // 移除消息监听器
  public removeMessageListener(listener: (message: Message) => void): void {
    this.messageListeners = this.messageListeners.filter(l => l !== listener);
  }

  // 添加在线状态监听器
  public addStatusListener(listener: (status: { userId: number; isOnline: boolean }) => void): void {
    this.statusListeners.push(listener);
  }

  // 移除在线状态监听器
  public removeStatusListener(listener: (status: { userId: number; isOnline: boolean }) => void): void {
    this.statusListeners = this.statusListeners.filter(l => l !== listener);
  }

  // 检查是否已连接
  public isConnected(): boolean {
    return this.socket?.connected || false;
  }
}

export const socketService = SocketService.getInstance(); 