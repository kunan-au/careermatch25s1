// SkillAnalysis.tsx

import { FC, useState } from 'react';
import { Button } from '@/components/ui/button';

interface SkillAnalysisProps {
  matchingSkills: string[];
  missingSkills: string[];
  associatedSkills: string[];
  advice: string;
}

const SkillAnalysis: FC<SkillAnalysisProps> = ({
  matchingSkills,
  missingSkills,
  associatedSkills,
  advice,
}) => {
  const [isExpanded, setIsExpanded] = useState(false);

  const toggleExpand = () => {
    setIsExpanded(!isExpanded);
  };

  return (
    <div className="bg-white p-6 shadow-md rounded-lg mt-4">
      <div className="flex items-center justify-between cursor-pointer" onClick={toggleExpand}>
        <h2 className="text-xl font-semibold">Skill Analysis</h2>
        <Button variant="ghost" size="icon">
          {isExpanded ? (
            <span className="text-gray-600">▲</span>
          ) : (
            <span className="text-gray-600">▼</span>
          )}
        </Button>
      </div>

      {isExpanded && (
        <div className="mt-4">
          <div className="mb-4">
            <h3 className="font-semibold text-green-700">Matching Skills:</h3>
            <ul className="list-disc ml-6 text-gray-700">
              {matchingSkills.map((skill, index) => (
                <li key={index}>{skill}</li>
              ))}
            </ul>
          </div>

          <div className="mb-4">
            <h3 className="font-semibold text-red-700">Missing Skills:</h3>
            <ul className="list-disc ml-6 text-gray-700">
              {missingSkills.map((skill, index) => (
                <li key={index}>{skill}</li>
              ))}
            </ul>
          </div>

          <div className="mb-4">
            <h3 className="font-semibold text-blue-700">Associated Skills:</h3>
            <ul className="list-disc ml-6 text-gray-700">
              {associatedSkills.map((skill, index) => (
                <li key={index}>{skill}</li>
              ))}
            </ul>
          </div>

          <div>
            <h3 className="font-semibold text-purple-700">Advice for Job Seeker:</h3>
            <p className="mt-2 whitespace-pre-line text-gray-700">{advice}</p>
          </div>
        </div>
      )}
    </div>
  );
};

export default SkillAnalysis;
