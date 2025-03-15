import { io, Socket } from 'socket.io-client';
import { Message } from '@/types/chat';

// Event type definitions
export enum SocketEvent {
  CONNECT = 'connect',
  DISCONNECT = 'disconnect',
  MESSAGE = 'message',
  TYPING = 'typing',
  ONLINE_STATUS = 'online_status',
  FILE_UPLOAD = 'file_upload',
}

// Socket service implementation using Singleton pattern
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

  // Connect to WebSocket server
  public connect(userId: number): void {
    // Using local WebSocket server for now
    // Can be replaced with actual backend WebSocket address in the future
    this.socket = io('http://localhost:8000', {
      query: { userId: userId.toString() },
    });

    // Set up event listeners
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

  // Disconnect from server
  public disconnect(): void {
    if (this.socket) {
      this.socket.disconnect();
      this.socket = null;
    }
  }

  // Send message
  public sendMessage(message: Omit<Message, 'id' | 'timestamp'>): void {
    if (this.socket) {
      this.socket.emit(SocketEvent.MESSAGE, message);
    } else {
      console.error('Socket not connected');
    }
  }

  // Send file message
  public sendFileMessage(file: File, fileName: string, type: 'file'): void {
    if (this.socket) {
      // In a real implementation, we would upload the file to a server
      // and then send the file URL in the message
      const fileReader = new FileReader();
      fileReader.readAsArrayBuffer(file);
      
      fileReader.onload = () => {
        const arrayBuffer = fileReader.result;
        this.socket?.emit(SocketEvent.FILE_UPLOAD, { 
          file: arrayBuffer, 
          fileName, 
          type 
        });
      };
    } else {
      console.error('Socket not connected');
    }
  }

  // Send typing status
  public sendTyping(isTyping: boolean, recipientId: number): void {
    if (this.socket) {
      this.socket.emit(SocketEvent.TYPING, { isTyping, recipientId });
    }
  }

  // Add message listener
  public addMessageListener(listener: (message: Message) => void): void {
    this.messageListeners.push(listener);
  }

  // Remove message listener
  public removeMessageListener(listener: (message: Message) => void): void {
    this.messageListeners = this.messageListeners.filter(l => l !== listener);
  }

  // Add online status listener
  public addStatusListener(listener: (status: { userId: number; isOnline: boolean }) => void): void {
    this.statusListeners.push(listener);
  }

  // Remove online status listener
  public removeStatusListener(listener: (status: { userId: number; isOnline: boolean }) => void): void {
    this.statusListeners = this.statusListeners.filter(l => l !== listener);
  }

  // Check if connected
  public isConnected(): boolean {
    return this.socket?.connected || false;
  }
}

export const socketService = SocketService.getInstance(); 