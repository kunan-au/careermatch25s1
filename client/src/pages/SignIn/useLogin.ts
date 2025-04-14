import { useMutation } from "@tanstack/react-query";
import axios from "axios";
import toast from "react-hot-toast";
import { api } from "@/services/api";

interface User {
  email: string;
  password: string;
  role: "recruiter" | "candidate";
}

interface SuccessResponse {
  access_token: string;
  refresh_token: string;
}

type LoginResponse = SuccessResponse | undefined;

const loginUser = async (user: User): Promise<LoginResponse> => {
  const response = await api.post("/auth/users/tokens", user);
  if (response.status === 200) {
    return response.data;
  }
  throw new Error(`Unexpected status code: ${response.status}`);
};

export function useLogin() {
  const {
    mutateAsync: login,
    status,
    data: userToken,
  } = useMutation<LoginResponse, Error, User>({
    mutationFn: loginUser,
    onSuccess: async (data, variables) => {
      localStorage.setItem("access_token", data?.access_token ?? "");

      try {
        const profile = await api.get(`/users/${variables.email}`);
        const realRole = profile.data.role;

        if (realRole !== variables.role) {
          throw new Error(
            `This account is registered as a "${realRole}". Please log in with the correct role.`
          );
        }

        localStorage.setItem("role", realRole);
        toast.success("Login successfully!");
      } catch (err: any) {
        const errorMessage = err?.message || "Failed to fetch user profile.";
        toast.error(errorMessage);
      }
    },
    onError: (err) => {
      if (axios.isAxiosError(err) && err.response?.data?.detail) {
        toast.error(err.response.data.detail);
      } else {
        toast.error(err.message || "Login failed. Please try again.");
      }
    },
  });

  return { status, login, userToken };
}
