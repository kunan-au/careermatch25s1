import { useMutation, useQueryClient } from "@tanstack/react-query";
import axios from "axios";
import toast from "react-hot-toast";
import { api } from "@/services/api";

type SuccessAvatarResponse = {
  message: string;
};

type AvatarResponse = SuccessAvatarResponse | undefined;

const uploadAvatar = async (
  email: string,
  file: File
): Promise<AvatarResponse> => {
  const formData = new FormData();
  formData.append("avatar", file);
  try {
    const response = await api.post(
      `/users/${encodeURIComponent(email)}/avatar`,
      formData,
      {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      }
    );

    // only 200 status code is considered as success
    if (response.status === 200) {
      return response.data;
    } else {
      throw new Error(`Unexpected status code: ${response.status}`);
    }
  } catch (error) {
    if (axios.isAxiosError(error)) {
      if (error.response && error.response.status === 422) {
        throw new Error(
          "The image you uploaded seems incorrect. Please check and try again later."
        );
      }
      throw new Error(
        "Something went wrong connecting to the server. Please try again later."
      );
    }
    throw error;
  }
};

export function useAvatarUpdate() {
  const queryClient = useQueryClient();
  const {
    mutateAsync: updateAvatar,
    status,
    data: responseData,
  } = useMutation<AvatarResponse, Error, { email: string; file: File }>({
    mutationFn: ({ email, file }) => uploadAvatar(email, file),
    onSuccess: (data) => {
      const email = data?.message.split(" ")[2];
      toast.success("You have successfully updated your avatar!");
      queryClient.invalidateQueries({ queryKey: ["profile", email] });
    },
    onError: (err) => {
      toast.error(err.message);
    },
  });

  return { status, updateAvatar, responseData };
}
