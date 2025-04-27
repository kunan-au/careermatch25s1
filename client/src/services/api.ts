import axios, { AxiosInstance } from "axios";
import { Message } from "@/types/chat";

interface CustomApi extends AxiosInstance {
  getMessages: () => Promise<{ data: Message[] }>;
  sendMessage: (message: string) => Promise<{ data: Message }>;
}

// Create base axios instance
const axiosInstance = axios.create({
  baseURL: "http://localhost:16000",
  withCredentials: true,
  headers: {
    Accept: "application/json",
  },
}) as CustomApi;

// Add custom methods
axiosInstance.getMessages = async () => {
  const response = await axiosInstance.get<Message[]>('/api/messaging/messages');
  return response;
};

axiosInstance.sendMessage = async (message: string) => {
  const response = await axiosInstance.post<Message>('/api/messaging/messages', { message });
  return response;
};

export const api = axiosInstance;
