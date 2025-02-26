import React from 'react';

interface FileMessageProps {
  fileName: string;
  fileUrl: string;
  timestamp: string;
  sender: string;
  formatTimestamp: (timestamp: string) => string;
}

const FileMessage: React.FC<FileMessageProps> = ({
  fileName,
  fileUrl,
  timestamp,
  formatTimestamp
}) => {
  // Get file extension
  const fileExtension = fileName.split('.').pop()?.toLowerCase() || '';
  
  // Determine file type icon based on extension
  const getFileIcon = () => {
    if (['jpg', 'jpeg', 'png', 'gif', 'bmp', 'svg'].includes(fileExtension)) {
      return (
        <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
          <path fillRule="evenodd" d="M4 3a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V5a2 2 0 00-2-2H4zm12 12H4l4-8 3 6 2-4 3 6z" clipRule="evenodd" />
        </svg>
      );
    } else if (['doc', 'docx', 'txt', 'pdf'].includes(fileExtension)) {
      return (
        <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
          <path fillRule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4z" clipRule="evenodd" />
        </svg>
      );
    } else {
      return (
        <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
          <path fillRule="evenodd" d="M8 4a3 3 0 00-3 3v4a3 3 0 006 0V7a1 1 0 112 0v4a5 5 0 01-10 0V7a5 5 0 0110 0v4a1 1 0 11-2 0V7a3 3 0 00-3-3z" clipRule="evenodd" />
        </svg>
      );
    }
  };

  return (
    <div className="flex flex-col">
      <div className="flex items-center space-x-2 mb-1">
        {getFileIcon()}
        <a 
          href={fileUrl} 
          target="_blank" 
          rel="noopener noreferrer" 
          className="text-sm font-medium underline hover:text-blue-600"
          download={fileName}
        >
          {fileName}
        </a>
      </div>
      <p className="text-xs opacity-70">
        {formatTimestamp(timestamp)}
      </p>
    </div>
  );
};

export default FileMessage; 