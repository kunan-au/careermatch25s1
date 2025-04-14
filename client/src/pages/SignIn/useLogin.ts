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
        localStorage.setItem("role", realRole);
      } catch {
        toast.error("Failed to fetch user profile.");
      }

      toast.success("Login successfully!");
    },
    onError: (err) => {
      toast.error(err.message);
    },
  });

  return { status, login, userToken };
}