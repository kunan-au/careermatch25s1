export const uploadResume = async (file: File): Promise<string> => {
    const formData = new FormData();
    formData.append('resume', file);
  
    try {
      const response = await fetch('/api/resume/upload', {
        method: 'POST',
        body: formData,
      });
  
      if (!response.ok) {
        throw new Error('Resume upload failed');
      }
  
      return 'Resume uploaded successfully';
    } catch (error) {
      throw new Error(error.message);
    }
  };
  