import axios from "axios";
import { useQuery } from "@tanstack/react-query";
import { api } from "@/services/api";

type UserData = {
  email: string;
  name: string;
  avatar: string;
  resume: string;
};

type UserResponse = UserData | undefined;

const fetchUserByEmail = async (email: string): Promise<UserResponse> => {
  try {
    const response = await api.get(`/users/${encodeURIComponent(email)}`);
    if (response.status === 200) {
      console.log(response.data);
      return response.data;
    } else {
      throw new Error(`Unexpected status code: ${response.status}`);
    }
  } catch (error) {
    if (axios.isAxiosError(error)) {
      if (error.response && error.response.status === 422) {
        throw new Error("Validation Error.");
      }
    }
    throw error;
  }
};

export function useProfile(email: string) {
  const {
    isLoading,
    data: user_info,
    fetchStatus,
    error,
  } = useQuery({
    queryKey: ["profile", email],
    queryFn: () => fetchUserByEmail(email),
  });

  return {
    isLoading,
    user_info,
    fetchStatus,
    error,
  };
}
