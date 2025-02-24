export interface Message {
  id: number;
  text: string;
  sender: string;
  timestamp: string;
  avatar?: string;
}

export interface ChatContact {
  id: number;
  name: string;
  title?: string;  // 比如 "Children's Book Illustrator"
  avatar?: string;
  lastMessage?: string;
  timestamp?: string;
  isOnline?: boolean;
} 