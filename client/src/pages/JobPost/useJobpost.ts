import { useMutation } from "@tanstack/react-query";
import axios from "axios";
import toast from "react-hot-toast";
import { api } from "@/services/api";

interface JobPostData {
  title: string;
  company: string;
  job_type: string;
  description: string;
}

interface JobPostSuccessResponse {
  id: string;
  title: string;
  company: string;
  job_type: string;
  description: string;
  created_at: string;
  updated_at: string;
}

type JobPostResponse = JobPostSuccessResponse | undefined;

const postJob = async (jobData: JobPostData): Promise<JobPostResponse> => {
  try {
    const response = await api.post<JobPostResponse>("/jobs/", jobData);

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

export function useJobPost() {
  const {
    mutateAsync: jobPost,
    status,
    data: responseData,
  } = useMutation<JobPostResponse, Error, JobPostData>({
    mutationFn: postJob,
    onSuccess: () => {
      toast.success("You have successfully posted a job!");
    },
    onError: (err) => {
      toast.error(err.message);
    },
  });

  return { status, jobPost, responseData };
}
