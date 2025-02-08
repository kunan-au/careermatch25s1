import { useQuery } from '@tanstack/react-query';
import axios from 'axios';
import { api } from "@/services/api";

// Define the interface to match the response from the backend API
interface JobDetail {
  id: string;
  title: string;
  company: string;
  job_type: string;
  description: string;
  created_at: string;
  updated_at: string;
}


type JobDetailResponse = JobDetail | undefined;

const getJobById = async (jobId: string): Promise<JobDetailResponse> => {
  try {
    const response = await api.get<JobDetail>(`/jobs/${jobId}`);
      if (response.status === 200) {
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
}
  
export function useJobDetail(jobId: string) {
    const {
      isLoading,
      data: job_detail,
      fetchStatus,
      error,
    } = useQuery({
      queryKey: ["job", jobId],
      queryFn: () => getJobById(jobId),
    });
  
    return {
      isLoading,
      job_detail,
      fetchStatus,
      error,
    };
}

