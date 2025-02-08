import { useMutation, useQueryClient } from "@tanstack/react-query";
import axios from "axios";
import toast from "react-hot-toast";
import { api } from "@/services/api";

type UserData = {
  email: string;
  name: string;
  avatar: string;
  resume: string;
};

type ProfileUpdateResponse = UserData | undefined;

const updateProfile = async (
  userData: UserData
): Promise<ProfileUpdateResponse> => {
  const { email, ...data } = userData;

  try {
    const response = await api.put(`/users/${encodeURIComponent(email)}`, data);

    // only 200 status code is considered as success
    if (response.status === 200) {
      console.log(response.data);
      return response.data;
    } else {
      throw new Error(`Unexpected status code: ${response.status}`);
    }
  } catch (error) {
    if (axios.isAxiosError(error)) {
      if (error.response && error.response.status === 422) {
        throw new Error(
          "The information you provided seems incorrect. Please check and try again later."
        );
      }
      throw new Error(
        "Something went wrong connecting to the server. Please try again later."
      );
    }
    throw error;
  }
};

export function useProfileUpdate() {
  const queryClient = useQueryClient();

  const {
    mutateAsync: profileUpdate,
    status,
    data: updatedProfile,
  } = useMutation<ProfileUpdateResponse, Error, UserData>({
    mutationFn: updateProfile,
    onSuccess: (data) => {
      toast.success("You have successfully updated your personal information!");
      queryClient.invalidateQueries({ queryKey: ["profile", data?.email] });
    },
    onError: (err) => {
      toast.error(err.message);
    },
  });

  return { status, profileUpdate, updatedProfile };
}
