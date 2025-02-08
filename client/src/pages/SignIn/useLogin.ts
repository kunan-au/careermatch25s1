import { useMutation } from "@tanstack/react-query";
import axios from "axios";
import toast from "react-hot-toast";
import { api } from "@/services/api";

interface User {
  email: string;
  password: string;
}

interface SuccessResponse {
  access_token: string;
  refresh_token: string;
}

type LoginResponse = SuccessResponse | undefined;

const loginUser = async (user: User): Promise<LoginResponse> => {
  try {
    const response = await api.post("/auth/users/tokens", user);

    // only 200 status code is considered as success
    if (response.status === 200) {
      return response.data;
    } else {
      throw new Error(`Unexpected status code: ${response.status}`);
    }
  } catch (error) {
    if (axios.isAxiosError(error)) {
      if (error.response && error.response.status === 401) {
        throw new Error(
          "Username or password is incorrect. Please check and try again."
        );
      }
      throw new Error(
        "Something went wrong connecting to the server. Please try again later."
      );
    }
    throw error;
  }
};

export function useLogin() {
  const {
    mutateAsync: login,
    status,
    data: userToken,
  } = useMutation<LoginResponse, Error, User>({
    mutationFn: loginUser,
    onSuccess: (data) => {
      console.log(data);
      // Save the access token to local storage
      localStorage.setItem(
        "access_token",
        data?.access_token ? data.access_token : ""
      );
      toast.success("Login successfully!");
    },
    onError: (err) => {
      toast.error(err.message);
    },
  });

  return { status, login, userToken };
}
