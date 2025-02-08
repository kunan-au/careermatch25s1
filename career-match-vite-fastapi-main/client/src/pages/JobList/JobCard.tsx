import { FC } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { useState } from "react";

interface JobProps {
  jobKey: string;
  jobTitle: string;
  jobType: string;
  jobField: string;
  location: string;
}

const JobCard: FC<JobProps> = ({
  jobTitle,
  jobField,
  jobType,
  location,
  jobKey,
}) => {
  const navigate = useNavigate();

  /************************************************************************************************************/
  const [isFavorited, setIsFavorited] = useState(false);

  const toggleFavorite = async () => {
    const newFavoriteStatus = !isFavorited;
    setIsFavorited(newFavoriteStatus);
    console.log(`Toggle favorite status for job ${jobKey}: ${newFavoriteStatus}`);
    // await sendFavoriteStatusToBackend(jobId, newFavoriteStatus);
  };
  /************************************************************************************************************/

  return (
    <>
      <div className="relative flex flex-col items-center justify-center overflow-hidden bg-gray-50 p-2 sm:py-4">
        <div className="bg-white shadow-l shadow-gray-100 w-full max-w-4xl flex flex-col sm:flex-row gap-3 sm:items-center justify-between px-5 py-4 rounded-md">
          <div>
            <span className="text-green-800 text-sm">{jobField}</span>
            <h3 className="font-bold mt-px">{jobTitle}</h3>
            <div className="flex items-center gap-3 mt-2">
              <span className="bg-green-100 text-green-700 rounded-full px-3 py-1 text-sm">
                {jobType}
              </span>
              <span className="text-slate-600 text-sm flex gap-1 items-center">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  className="h-4 w-4"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                  strokeWidth="2"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"
                  />
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"
                  />
                </svg>
                {location}
              </span>
            </div>
          </div>
          <div className="flex gap-2">
            <Button onClick={toggleFavorite} className={`ml-5 p-2 border-2 border-red-500 bg-white hover:bg-transparent hover:text-red-700 ${isFavorited ? 'text-red-500' : 'text-gray-400'}`}>
            {isFavorited ? '♥' : '♡'} 
            </Button>
            <button
              className="bg-green-600 text-white font-medium px-4 py-2 rounded-md flex gap-1 items-center"
              onClick={() => {
                navigate(`/jobs/${jobKey}`);
                // navigate("test-jobID");
              }}
            >
              Apply Now
              <svg
                xmlns="http://www.w3.org/2000/svg"
                className="h-4 w-4"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                strokeWidth="2"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  d="M13 7l5 5m0 0l-5 5m5-5H6"
                />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </>
  );
};

export default JobCard;
