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

// 请求拦截器 - 自动添加token
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

// 响应拦截器 - 处理401错误
axiosInstance.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    
    // 如果是401错误且不是刷新token的请求
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      try {
        // 尝试刷新token
        const refreshToken = localStorage.getItem("refresh_token");
        if (refreshToken) {
          const response = await axiosInstance.put("/auth/users/tokens", {});
          
          if (response.data?.access_token) {
            localStorage.setItem("access_token", response.data.access_token);
            
            // 使用新token重试原始请求
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
