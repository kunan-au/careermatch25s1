// useJobDetail.ts

import { useQuery } from '@tanstack/react-query';
import { mockJobs } from '../JobList/useJobList'; // Adjusted import

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
  // Find the job in the mock data
  const job = mockJobs.find((job) => job.id === jobId);
  return job;
};

export function useJobDetail(jobId: string) {
  const {
    isLoading,
    data: job_detail,
    error,
  } = useQuery({
    queryKey: ["job", jobId],
    queryFn: () => getJobById(jobId),
  });

  return {
    isLoading,
    job_detail,
    error,
  };
}
