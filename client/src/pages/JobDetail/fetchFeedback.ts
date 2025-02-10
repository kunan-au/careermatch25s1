// fetchFeedback.ts

import axios from 'axios';

export const fetchFeedback = async (jobId: string): Promise<string> => {
  try {
    const response = await axios.get(`/api/feedback/${jobId}`);
    return response.data.feedback;
  } catch (error) {
    throw new Error('Failed to fetch feedback');
  }
};
