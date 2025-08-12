import axios, { AxiosInstance } from "axios";
import { Message } from "@/types/chat";

interface CustomApi extends AxiosInstance {
  getMessages: () => Promise<{ data: Message[] }>;
  sendMessage: (message: string) => Promise<{ data: Message }>;
}

// Create base axios instance
const axiosInstance = axios.create({
  baseURL: "http://localhost:8000",
  withCredentials: true,
  headers: {
    Accept: "application/json",
  },
}) as CustomApi;

// Request interceptor - automatically add token
axiosInstance.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("access_token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor - handle 401 errors
axiosInstance.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    
    // If it's a 401 error and not a token refresh request
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      try {
        // Try to refresh token
        const refreshToken = localStorage.getItem("refresh_token");
        if (refreshToken) {
          const response = await axiosInstance.put("/auth/users/tokens", {});
          
          if (response.data?.access_token) {
            localStorage.setItem("access_token", response.data.access_token);
            
            // Retry original request with new token
            originalRequest.headers.Authorization = `Bearer ${response.data.access_token}`;
            return axiosInstance(originalRequest);
          }
        }
      } catch (refreshError) {
        console.error("Token refresh failed:", refreshError);
      }
    }
    
    return Promise.reject(error);
  }
);

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
