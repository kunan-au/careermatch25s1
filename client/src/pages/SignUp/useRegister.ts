import { useMutation } from "@tanstack/react-query";
import axios from "axios";
import toast from "react-hot-toast";
import { api } from "@/services/api";

interface User {
  email: string;
  password: string;
}

interface SuccessResponse {
  email: string;
}

type RegisterResponse = SuccessResponse | undefined;

const registerUser = async (user: User): Promise<RegisterResponse> => {
  try {
    const response = await api.post("/auth/users", user, {
      timeout: 3000,
    });

    // only 201 status code is considered as success
    if (response.status === 201) {
      return response.data;
    } else {
      throw new Error(`Unexpected status code: ${response.status}`);
    }
  } catch (error) {
    if (axios.isAxiosError(error)) {
      if (error.response && error.response.status === 400) {
        throw new Error(
          "This email has already been used. Please use another email and try again."
        );
      }
      if (error.response && error.response.status === 422) {
        throw new Error(
          "The email address or password seems incorrect. Please check them and try again."
        );
      }
      throw new Error(
        "Something went wrong connecting to the server. Please try again later."
      );
    }
    throw error;
  }
};

export function useRegister() {
  const { mutateAsync: register, status } = useMutation<
    RegisterResponse,
    Error,
    User
  >({
    mutationFn: registerUser,
    onSuccess: (data) => {
      console.log(data);
      toast.success(
        "You have successfully registered! Please sign in to continue!"
      );
    },
    onError: (err) => {
      toast.error(err.message);
    },
  });

  return { status, register };
}
