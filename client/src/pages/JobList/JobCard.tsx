import { FC, useState, useEffect } from 'react';
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
  const [isFavorited, setIsFavorited] = useState(false); // State to track if the job is favorited
  const [isDisliked, setIsDisliked] = useState(false); // State to track if the job is disliked
  const [showConfirmDialog, setShowConfirmDialog] = useState(false); // State to control the confirmation dialog visibility
  const [matchScore, setMatchScore] = useState(0); // State to store the match score

  useEffect(() => {
    // Generate a random match score between 50 and 100
    setMatchScore(Math.floor(Math.random() * 51) + 50);
  }, []);

  // Toggle the favorite status
  const toggleFavorite = () => {
    setIsFavorited(!isFavorited);
  };

  // Handle the dislike action after confirmation
  const handleDislike = () => {
    setIsDisliked(true); // Mark the job as disliked
    setShowConfirmDialog(false); // Close the confirmation dialog
  };

  // Open the confirmation dialog
  const openConfirmDialog = () => {
    setShowConfirmDialog(true);
  };

  // Close the confirmation dialog
  const closeConfirmDialog = () => {
    setShowConfirmDialog(false);
  };

  // If the job is disliked, do not render the card
  if (isDisliked) return null;

  return (
    <div className="relative flex flex-col items-center justify-center overflow-hidden bg-gray-50 p-2 sm:py-4">
      <div className="bg-white shadow-l shadow-gray-100 w-full max-w-4xl flex flex-col sm:flex-row gap-3 sm:items-center justify-between px-5 py-4 rounded-md">
        <div className="flex-1">
          {/* Job field and title */}
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

        {/* Match score progress bar */}
        <div className="flex flex-col items-center">
          <span className="text-gray-600 text-sm">Job Match Score</span>
          <div className="relative w-24 h-3 bg-gray-200 rounded-full overflow-hidden">
            <div
              className="h-full bg-green-500"
              style={{ width: `${matchScore}%` }}
            ></div>
          </div>
          <span className="text-sm text-gray-700">{matchScore}%</span>
        </div>

        {/* Action buttons */}
        <div className="flex gap-2 items-center">
          {/* Favorite button */}
          <button
            onClick={toggleFavorite}
            className="text-2xl transition-colors"
          >
            {isFavorited ? '❤️' : '🤍'}
          </button>

          {/* Dislike button */}
          <button
            onClick={openConfirmDialog}
            className="text-2xl text-red-400 hover:text-red-600 transition-colors"
          >
            👎
          </button>

          {/* Apply button */}
          <button
            className="bg-green-600 text-white font-medium px-4 py-2 rounded-md flex gap-1 items-center"
            onClick={() => navigate(`/jobs/${jobKey}`)}
          >
            Apply Now
          </button>
        </div>
      </div>

      {/* Confirmation dialog */}
      {showConfirmDialog && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white p-6 rounded-lg shadow-lg w-80">
            <h2 className="text-lg font-bold mb-4">Confirm Dislike</h2>
            <p className="text-gray-600 mb-6">Are you sure you want to dislike this job?</p>
            <div className="flex justify-end gap-4">
              {/* Cancel button */}
              <button
                onClick={closeConfirmDialog}
                className="px-4 py-2 bg-gray-200 text-gray-700 rounded hover:bg-gray-300"
              >
                Cancel
              </button>
              {/* Confirm button */}
              <button
                onClick={handleDislike}
                className="px-4 py-2 bg-green-600 text-white rounded hover:bg-red-600"
              >
                Confirm
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default JobCard;
