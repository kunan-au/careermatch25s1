import JobCard from "./JobCard";

export interface Job {
  id: string;
  title: string;
  company: string;
  job_type: string;
  created_at: string;
  updated_at: string;
}

interface ListProps {
  heading: string;
  jobs: Job[];
}

const jobType: { [key: string]: string } = {
  ft: "Full Time",
  pt: "Part Time",
  cv: "Casual/Vacation",
  ct: "Contract/Temp",
};

export default function JobListInfo({ heading, jobs }: ListProps) {
  return (
    <>
      <h1 className="w-full text-center text-3xl font-bold bg-gray-50 py-10">
        {heading}
      </h1>
      {jobs.map((jobItem, index) => (
        <JobCard
          key={index}
          jobKey={jobItem.id}
          jobTitle={jobItem.title}
          jobType={jobType[jobItem.job_type]}
          jobField="Engineering"
          location={jobItem.company}
        />
      ))}
    </>
  );
}
