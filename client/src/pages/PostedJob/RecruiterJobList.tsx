import { useSearchParams } from 'react-router-dom';
import Pagination from './RecruiterPagination.tsx';
import { PAGE_SIZE } from '../../utils/constants';
import RecruiterJobListInfo from './RecruiterJobListInfo.tsx';
import { useUser } from '../SignIn/useUser';
import { useJobList } from './RecruiteruseJobList.ts';
import { Skeleton } from '@/components/ui/skeleton';

export default function RecruiterJobList() {
  const { user_profile } = useUser();
  const { email } = user_profile ? user_profile : { email: "recruiter@example.com" };

  const { isLoading, job_list } = useJobList(email);

  const jobsCount = job_list?.length || 0;

  const [searchParams] = useSearchParams();
  const page = !searchParams.get("page") ? 1 : Number(searchParams.get("page"));
  const pageCount = Math.ceil(jobsCount / PAGE_SIZE);
  const pagedJobs =
    page === pageCount
      ? job_list?.slice(PAGE_SIZE * (page - 1))
      : job_list?.slice(PAGE_SIZE * (page - 1), PAGE_SIZE * page);

  return isLoading ? (
    <Skeleton />
  ) : (
    <>
      <RecruiterJobListInfo heading="Jobs You Posted" jobs={pagedJobs || []} />
      <div className="flex w-full justify-center py-8 bg-gray-50">
        <Pagination totalItemsCount={jobsCount} />
      </div>
    </>
  );
}
