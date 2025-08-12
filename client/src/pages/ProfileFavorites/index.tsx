import { useState, useEffect } from "react";
import JobListInfo from "../JobList/JobListInfo";
import { Job } from "../JobList/useJobList";

export default function ProfileFavorites() {
  const [favoriteJobs, setFavoriteJobs] = useState<Job[]>([]);

  // from localStorage
  const loadFavoriteJobs = () => {
    const favorites = JSON.parse(localStorage.getItem('favoriteJobs') || '[]');
    const jobsWithRequiredFields = favorites.map((job: any) => ({
      ...job,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
      description: job.description || "No description available"
    }));
    setFavoriteJobs(jobsWithRequiredFields);
  };

  useEffect(() => {

    loadFavoriteJobs();

    const handleStorageChange = (e: StorageEvent) => {
      if (e.key === 'favoriteJobs') {
        loadFavoriteJobs();
      }
    };

    window.addEventListener('storage', handleStorageChange);

    return () => {
      window.removeEventListener('storage', handleStorageChange);
    };
  }, []);

  return <JobListInfo heading="Favorite Jobs" jobs={favoriteJobs} />;
}