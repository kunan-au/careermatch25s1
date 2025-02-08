import { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Skeleton } from '@/components/ui/skeleton';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { useJobDetail } from './useJobDetail';

export default function JobDetail() {
  const { id } = useParams<{ id?: string }>();
  const navigate = useNavigate();
  const { isLoading, job_detail: jobDetail, error } = useJobDetail(id || '0');
  const [resumeFile, setResumeFile] = useState<File | null>(null);
  const [feedback, setFeedback] = useState('Waiting for feedback...');
  const [isUploading, setIsUploading] = useState(false);

  const handleResumeUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setIsUploading(true);
      const file = e.target.files[0];
      try {
        await uploadResume(file);
        setResumeFile(file);
        alert('Resume uploaded successfully!');
      } catch (error) {
        alert(error.message);
      } finally {
        setIsUploading(false);
      }
    }
  };

  const handleFeedbackFetch = async () => {
    try {
      const feedback = await fetchFeedback(id || '0');
      setFeedback(feedback);
    } catch (error) {
      alert('Error fetching feedback');
    }
  };

  if (isLoading) return <Skeleton />;

  if (error) return <div>Error: {error.message}</div>;

  if (!jobDetail) return <div>Job not found</div>;

  return (
    <div className="container mx-auto p-4">
      <div className="bg-white shadow-lg rounded-lg overflow-hidden">
        <div className="p-6">
          <h2 className="text-2xl font-bold text-green-600">{jobDetail.title}</h2>
          <p className="text-gray-700">{jobDetail.description}</p>
        </div>

        <div className="flex p-6">
          {/* Resume Upload */}
          <div className="w-1/2 p-4 bg-gray-100">
            <h3 className="text-xl font-semibold text-green-600">Upload Resume</h3>
            <Input
              type="file"
              accept=".pdf"
              onChange={handleResumeUpload}
              className="mt-4"
              disabled={isUploading}
            />
            {resumeFile && <p className="mt-2 text-sm text-gray-600">{resumeFile.name}</p>}
          </div>

          {/* Right Feedback Return */}
          <div className="w-1/2 p-4">
            <h3 className="text-xl font-semibold text-green-600">Feedback</h3>
            <Textarea
              value={feedback}
              readOnly
              className="mt-4 h-32"
            />
            <Button onClick={handleFeedbackFetch} className="mt-4 bg-green-600 text-white">
              Fetch Feedback
            </Button>
          </div>
        </div>
        <Button className="m-4 bg-green-600 text-white" onClick={() => navigate(-1)}>
          Go Back
        </Button>
      </div>
    </div>
  );
}
