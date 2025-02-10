// JobDetail/index.tsx

import { useParams, useNavigate } from 'react-router-dom';
import { useEffect, useState } from 'react';
import { Skeleton } from '@/components/ui/skeleton';
import { Button } from '@/components/ui/button';
import { useJobDetail } from './useJobDetail';
import SkillAnalysis from './SkillAnalysis';

interface SkillAnalysisData {
  matchingSkills: string[];
  missingSkills: string[];
  associatedSkills: string[];
  advice: string;
}

export default function JobDetail() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();

  const { isLoading, job_detail, error } = useJobDetail(id || '');
  const [skillAnalysisData, setSkillAnalysisData] = useState<SkillAnalysisData | null>(null);

  useEffect(() => {
    if (job_detail) {
      // Customize the skill analysis data based on the job details
      setSkillAnalysisData({
        matchingSkills: [
          'Proficiency in JavaScript',
          'Experience with React.js',
        ],
        missingSkills: [
          'Knowledge of cloud platforms (AWS or Azure)',
          'Experience with Docker and Kubernetes',
        ],
        associatedSkills: [
          'Familiarity with TypeScript',
          'Understanding of CI/CD pipelines',
        ],
        advice: `1. Consider learning about cloud platforms like AWS or Azure.\n2. Gain experience with Docker and Kubernetes.\n3. Explore TypeScript to enhance your skill set.`,
      });
    }
  }, [job_detail]);

  if (isLoading) {
    return <Skeleton />;
  }

  if (error || !job_detail) {
    return <div>Error loading job details or Job not found.</div>;
  }

  return (
    <div className="container mx-auto p-4">
      <div className="bg-white shadow-lg rounded-lg overflow-hidden">
        <div className="p-6">
          <h2 className="text-2xl font-bold text-green-600">{job_detail.title}</h2>
          <p className="text-gray-700 mb-4">
            <strong>Company:</strong> {job_detail.company}
          </p>
          <p className="text-gray-700 mb-4">
            <strong>Job Type:</strong>{' '}
            {job_detail.job_type === 'ft'
              ? 'Full Time'
              : job_detail.job_type === 'pt'
              ? 'Part Time'
              : 'Contract/Temp'}
          </p>
          <p className="text-gray-700 mb-4">
            <strong>Created At:</strong> {job_detail.created_at}
          </p>
          <p className="text-gray-700 mb-4">
            <strong>Last Updated:</strong> {job_detail.updated_at}
          </p>
          <p className="text-gray-700 mb-4">
            <strong>Description:</strong> {job_detail.description}
          </p>

          {skillAnalysisData && (
            <SkillAnalysis
              matchingSkills={skillAnalysisData.matchingSkills}
              missingSkills={skillAnalysisData.missingSkills}
              associatedSkills={skillAnalysisData.associatedSkills}
              advice={skillAnalysisData.advice}
            />
          )}

          <Button className="mt-4 bg-green-600 text-white" onClick={() => navigate(-1)}>
            Go Back
          </Button>
        </div>
      </div>
    </div>
  );
}
