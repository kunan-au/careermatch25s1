import JobListInfo from "../JobList/JobListInfo";

const favoriteJobs = [
  {
    id: "dcc0fc77-a5b0-4c3b-8d5a-1ee7f87a1369",
    title: "Senior Full Stack Backend Engineer",
    job_type: "ft",
    company: "Canberra, Australia",
    created_at: "2024-04-24T05:16:52.034Z",
    updated_at: "2024-04-24T05:16:52.034Z",
  },
  {
    id: "1a35295b-af34-405d-bb23-a9954a45e0c5",
    title: "Junior Frontend Developer",
    job_type: "pt",
    company: "Sydney, Australia",
    created_at: "2024-04-24T05:16:52.034Z",
    updated_at: "2024-04-24T05:16:52.034Z",
  },
  {
    id: "0d78c05d-1141-4bfe-819a-5632eada9afc",
    title: "Data Scientist",
    job_type: "ft",
    company: "Melbourne, Australia",
    created_at: "2024-04-24T05:16:52.034Z",
    updated_at: "2024-04-24T05:16:52.034Z",
  },
];

export default function ProfileFavorites() {
  return <JobListInfo heading="Favorite Jobs" jobs={favoriteJobs} />;
}
