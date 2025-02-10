// JobList/index.tsx
import { useSearchParams } from 'react-router-dom';
import Pagination from './Pagination';
import { PAGE_SIZE } from '../../utils/constants';
import JobListInfo from './JobListInfo';
import { useUser } from '../SignIn/useUser';
import { useJobList } from './useJobList';
import { Skeleton } from '@/components/ui/skeleton';

export default function JobList() {
  const { user_profile } = useUser();
  const { email } = user_profile ? user_profile : { email: "user@example.com" };

  // Fetch job list based on the user's email
  const { isLoading, job_list } = useJobList(email);

  const jobsCount = job_list?.length || 0;

  // For pagination
  const [searchParams] = useSearchParams();
  const page = !searchParams.get("page") ? 1 : Number(searchParams.get("page"));
  const pageCount = Math.ceil(jobsCount / PAGE_SIZE);
  const pagedJobs =
    page === pageCount
      ? job_list?.slice(PAGE_SIZE * (page - 1))
      : job_list?.slice(PAGE_SIZE * (page - 1), PAGE_SIZE * page);

  // Display skeleton loader while fetching jobs
  return isLoading ? (
    <Skeleton />
  ) : (
    <>
      {/* Job list information */}
      <JobListInfo heading="Here are your recommended jobs" jobs={pagedJobs || []} />
      <div className="flex w-full justify-center py-8 bg-gray-50">
        {/* Pagination component */}
        <Pagination totalItemsCount={jobsCount} />
      </div>
    </>
  );
}
