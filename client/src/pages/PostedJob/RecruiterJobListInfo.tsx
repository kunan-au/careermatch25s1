import RecruiterJobCard from './RecruiterJobCard';
import { Job } from './RecruiteruseJobList';

interface ListProps {
  heading: string;
  jobs: Job[];
}

const jobType: { [key: string]: string } = {
  ft: "Full Time",
  pt: "Part Time",
  ct: "Contract/Temp",
};

export default function RecruiterJobListInfo({ heading, jobs }: ListProps) {
  return (
    <>
      <h1 className="w-full text-center text-3xl font-bold bg-gray-50 py-10">
        {heading}
      </h1>
      {jobs.length === 0 ? (
        <p className="text-center">No jobs available at the moment</p>
      ) : (
        jobs.map((jobItem, index) => (
          <RecruiterJobCard
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
