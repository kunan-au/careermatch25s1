// JobListInfo.tsx

import JobCard from './JobCard';
import { Job } from './useJobList';

interface ListProps {
  heading: string;
  jobs: Job[];
}

const jobType: { [key: string]: string } = {
  ft: "Full Time",
  pt: "Part Time",
  ct: "Contract/Temp",
};

export default function JobListInfo({ heading, jobs }: ListProps) {
  console.log("Jobs passed to JobListInfo:", jobs); // Add this log to check jobs

  return (
    <>
      <h1 className="w-full text-center text-3xl font-bold bg-gray-50 py-10">
        {heading}
      </h1>
      {jobs.length === 0 ? (
        <p className="text-center">No jobs available at the moment</p>
      ) : (
        jobs.map((jobItem, index) => (
          <JobCard
            key={index}
            jobKey={jobItem.id}
            jobTitle={jobItem.title}
            jobType={jobType[jobItem.job_type]}
            jobField="Engineering"
            location={jobItem.company}
          />
        ))
      )}
    </>
  );
}
