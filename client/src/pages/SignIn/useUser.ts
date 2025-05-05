import axios from "axios";
import { useQuery } from "@tanstack/react-query";
import { api } from "@/services/api";

interface SuccessResponse {
  access_token: string;
  refresh_token: string;
}

type UpdateResponse = SuccessResponse | undefined;

async function updateTokens(): Promise<UpdateResponse> {
  // 首先检查localStorage中是否有refresh_token
  const refreshToken = localStorage.getItem("refresh_token");
  if (!refreshToken) {
    console.log("No refresh token found in localStorage");
    return undefined;
  }

  try {
    const response = await api.put("/auth/users/tokens", {});
    console.log("Token update response:", response.data);
    
    // 保存新的token
    if (response.data?.access_token) {
      localStorage.setItem("access_token", response.data.access_token);
    }
    if (response.data?.refresh_token) {
      localStorage.setItem("refresh_token", response.data.refresh_token);
    }
    
    return response.data;
  } catch (error) {
    console.error("Error updating tokens:", error);
    return undefined;
  }
}

interface UserResponse {
  email: string;
}

type AuthResponse = UserResponse | undefined;

async function getUserProfile(): Promise<AuthResponse> {
  try {
    // 首先检查localStorage中是否有access_token
    let accessToken = localStorage.getItem("access_token");
    
    // 如果没有access_token，尝试更新token
    if (!accessToken) {
      console.log("No access token in localStorage, trying to refresh");
      const responseFromUpdateTokens = await updateTokens();
      accessToken = responseFromUpdateTokens?.access_token ?? null;
      if (!accessToken) {
        console.log("Failed to get access token from refresh");
        return undefined;
      }
    }

    // 使用token请求用户信息
    const response = await api.get<AuthResponse>("/auth/users/me", {
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    });

    if (response.status === 200) {
      return response.data;
    } else {
      throw new Error(`Unexpected status code: ${response.status}`);
    }
  } catch (error) {
    console.error("Error in getUserProfile:", error);
    
    // 如果是401错误，尝试刷新token并重试一次
    if (axios.isAxiosError(error) && error.response?.status === 401) {
      try {
        const refreshResult = await updateTokens();
        if (refreshResult?.access_token) {
          // 用新token重试
          const retryResponse = await api.get<AuthResponse>("/auth/users/me", {
            headers: {
              Authorization: `Bearer ${refreshResult.access_token}`,
            },
          });
          if (retryResponse.status === 200) {
            return retryResponse.data;
          }
        }
      } catch (retryError) {
        console.error("Retry failed:", retryError);
      }
      
      // 如果重试也失败，清除token
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
      return undefined;
    }
    
    return undefined;
  }
}

export function useUser() {
  const {
    isLoading,
    data: user_profile,
    fetchStatus,
    error,
  } = useQuery({
    queryKey: ["user"],
    queryFn: getUserProfile,
    retry: 1,
    retryDelay: 1000,
  });

  return {
    isLoading,
    user_profile,
    fetchStatus,
    error,
    isAuthenticated: Boolean(user_profile),
  };
}
