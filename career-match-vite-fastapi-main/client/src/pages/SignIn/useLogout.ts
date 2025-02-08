import { useMutation } from "@tanstack/react-query";
import axios from "axios";
import toast from "react-hot-toast";
import { api } from "@/services/api";

const logoutUser = async () => {
  try {
    const response = await api.delete("/auth/users/tokens");

    // only 200 status code is considered as success
    if (response.status === 200) {
      return response.data;
    } else {
      throw new Error(`Unexpected status code: ${response.status}`);
    }
  } catch (error) {
    if (axios.isAxiosError(error)) {
      throw new Error(
        "Something went wrong logging out. Please try again later."
      );
    }
    throw error;
  }
};

export function useLogout() {
  const { mutateAsync: logout, status } = useMutation<Error>({
    mutationFn: logoutUser,
    onSuccess: (data) => {
      console.log(data);

      toast.success("Logout successfully!");
    },
    onError: (err) => {
      toast.error(err.message);
    },
  });

  return { status, logout };
}
