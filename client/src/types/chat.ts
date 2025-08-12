export interface Message {
  id: number;
  text?: string;  // Optional text message
  sender: string;
  timestamp: string;
  avatar?: string;
  audioUrl?: string;  // Voice message URL
  type?: 'text' | 'audio' | 'file';  // Message type
  fileUrl?: string;  // File URL
  fileName?: string;  // File name
}

export interface ChatContact {
  id: number;
  name: string;
  title?: string;  // e.g. "Software Engineer"
  avatar?: string;
  lastMessage?: string;
  timestamp?: string;
  isOnline?: boolean;
  unread?: boolean;
  isConnection?: boolean;
} 