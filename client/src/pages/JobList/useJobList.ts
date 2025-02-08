import { api } from "@/services/api";
import { Job } from "./JobListInfo";
import axios from "axios";
import { useQuery } from "@tanstack/react-query";

const listJob = async (email: string) : Promise<Job[]> => {
  try {
    const response = await api.get(`/jobs/recommendations/${encodeURIComponent(email)}`);
    if (response.status === 200) {
      return response.data;
    } else {
      throw new Error(`Unexpected status code: ${response.status}`);
    }
  } catch (error) {
    if (axios.isAxiosError(error)) {
      throw new Error(
        "Something went wrong. Please try again later."
      );
    }
    throw error;
  }
};

export function useJobList(email: string) {
  const {
    isLoading,
    data: job_list,
    fetchStatus,
    error,
  } = useQuery<Job[], Error>({
    queryKey: ["job", email],
    queryFn: () => listJob(email),
  });

  return {
    isLoading,
    job_list,
    fetchStatus,
    error,
  };
}