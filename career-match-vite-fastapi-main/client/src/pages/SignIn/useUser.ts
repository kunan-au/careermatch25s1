import axios from "axios";
import { useQuery } from "@tanstack/react-query";
import { api } from "@/services/api";

interface SuccessResponse {
  access_token: string;
  refresh_token: string;
}

type UpdateResponse = SuccessResponse | undefined;

async function updateTokens(): Promise<UpdateResponse> {
  try {
    const response = await api.put("/auth/users/tokens", {});
    console.log("Response:", response.data);
    return response.data;
  } catch (error) {
    console.error("Error:", error);
  }
}

interface UserResponse {
  email: string;
}

type AuthResponse = UserResponse | undefined;

async function getUserProfile(): Promise<AuthResponse> {
  try {
    const responseFromUpdateTokens = await updateTokens();
    const accessToken = responseFromUpdateTokens?.access_token;
    if (!accessToken) {
      throw new Error("No access token returned from updateTokens");
    }

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
    if (axios.isAxiosError(error)) {
      if (error.response && error.response.status === 401) {
        throw new Error("Please first login to access this page.");
      }
      throw new Error(
        "Something went wrong connecting to the server. Please try again later."
      );
    }
    throw error;
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
  });

  return {
    isLoading,
    user_profile,
    fetchStatus,
    error,
    isAuthenticated: Boolean(user_profile),
  };
}
