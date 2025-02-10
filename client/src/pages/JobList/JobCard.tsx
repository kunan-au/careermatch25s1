// JobCard.tsx

import { FC, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '@/components/ui/button';

interface JobProps {
  jobKey: string;
  jobTitle: string;
  jobType: string;
  jobField: string;
  location: string;
}

const JobCard: FC<JobProps> = ({ jobKey, jobTitle, jobType, jobField, location }) => {
  const navigate = useNavigate();
  const [isFavorited, setIsFavorited] = useState(false);

  const toggleFavorite = () => {
    setIsFavorited(!isFavorited);
  };

  return (
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
              {location}
            </span>
          </div>
        </div>
        <div className="flex gap-2">
          <Button 
            onClick={toggleFavorite} 
            className={`ml-5 p-2 border-2 border-red-500 bg-white hover:bg-transparent hover:text-red-700 ${isFavorited ? 'text-red-500' : 'text-gray-400'}`}>
            {isFavorited ? '♥' : '♡'}
          </Button>
          <button
            className="bg-green-600 text-white font-medium px-4 py-2 rounded-md flex gap-1 items-center"
            onClick={() => navigate(`/jobs/${jobKey}`)}
          >
            Apply Now
          </button>
        </div>
      </div>
    </div>
  );
};

export default JobCard;
