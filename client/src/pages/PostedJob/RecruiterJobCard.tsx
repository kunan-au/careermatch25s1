import { FC } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '@/components/ui/button';

interface JobProps {
  jobKey: string;
  jobTitle: string;
  jobType: string;
  jobField: string;
  location: string;
}

const RecruiterJobCard: FC<JobProps> = ({ jobKey, jobTitle, jobType, jobField, location }) => {
  const navigate = useNavigate();

  return (
    <div className="relative flex flex-col items-center justify-center overflow-hidden bg-gray-50 p-2 sm:py-4">
      <div className="bg-white shadow-l shadow-gray-100 w-full max-w-4xl flex flex-col sm:flex-row gap-3 sm:items-center justify-between px-5 py-4 rounded-md">
        <div className="flex-1">
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
            className="bg-green-600 text-white font-medium px-4 py-2 rounded-md flex gap-1 items-center"
            onClick={() => navigate(`/jobs/${jobKey}`)}
          >
            View
          </Button>
        </div>
      </div>
    </div>
  );
};

export default RecruiterJobCard;
