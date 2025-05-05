import { useState, useEffect } from 'react';
import { saveFeedback, getFeedback, MessageFeedback as IMessageFeedback } from '@/services/chatHistoryService';
import styles from './MessageFeedback.module.css';

interface MessageFeedbackProps {
  messageId: string;
}

const MessageFeedback = ({ messageId }: MessageFeedbackProps) => {
  const [feedback, setFeedback] = useState<'helpful' | 'unhelpful' | null>(null);
  const [showCommentInput, setShowCommentInput] = useState(false);
  const [comment, setComment] = useState('');
  const [submitted, setSubmitted] = useState(false);

  // Load existing feedback
  useEffect(() => {
    const existingFeedback = getFeedback(messageId);
    if (existingFeedback) {
      setFeedback(existingFeedback.rating);
      setComment(existingFeedback.comment || '');
      setSubmitted(true);
    }
  }, [messageId]);

  const handleFeedback = (rating: 'helpful' | 'unhelpful') => {
    // If clicking the same rating, toggle it off
    if (feedback === rating) {
      setFeedback(null);
      
      if (submitted) {
        // Remove the feedback from storage
        saveFeedback({
          messageId,
          rating: rating, // Keep the rating for database record
          comment: ''
        });
      }
    } else {
      setFeedback(rating);
      
      // Show comment input if rating is unhelpful
      if (rating === 'unhelpful') {
        setShowCommentInput(true);
      } else {
        submitFeedback(rating);
      }
    }
  };

  const submitFeedback = (rating: 'helpful' | 'unhelpful', userComment?: string) => {
    const feedbackData: IMessageFeedback = {
      messageId,
      rating,
      comment: userComment !== undefined ? userComment : comment
    };
    
    saveFeedback(feedbackData);
    setSubmitted(true);
    
    // Hide comment input if no comment was given
    if (!userComment && !comment) {
      setShowCommentInput(false);
    }
    
    // You might also want to send this feedback to your backend
    // api.post('/api/feedback', feedbackData);
  };

  const handleSubmitComment = () => {
    if (feedback) {
      submitFeedback(feedback);
    }
  };

  const handleCancel = () => {
    setShowCommentInput(false);
    if (!submitted) {
      setFeedback(null);
    }
  };

  return (
    <div className={styles.container}>
      {!submitted ? (
        <div className={styles.buttons}>
          <span className={styles.prompt}>Was this response helpful?</span>
          <button 
            className={`${styles.feedbackBtn} ${feedback === 'helpful' ? styles.active : ''}`}
            onClick={() => handleFeedback('helpful')}
            aria-label="Helpful"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M7 10v12M21 8a2 2 0 0 0-2-2h-6.31l.95-4.57.03-.32a1 1 0 0 0-.87-.7.996.996 0 0 0-.6.13L4.95 6.5a1 1 0 0 0-.32.48L3 12v6a2 2 0 0 0 2 2h8.59c.47 0 .9-.19 1.21-.5l.2-.5 4.8-8.8c.2-.53.3-1.3.2-2.2z" />
            </svg>
          </button>
          <button 
            className={`${styles.feedbackBtn} ${feedback === 'unhelpful' ? styles.active : ''}`}
            onClick={() => handleFeedback('unhelpful')}
            aria-label="Unhelpful"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M17 14V2M3 16a2 2 0 0 0 2 2h6.31l-.95 4.57-.03.32a1 1 0 0 0 .28.7c.18.19.41.29.67.29.23 0 .47-.09.63-.24L19.05 17.5a2 2 0 0 0 .32-.48L21 12V6a2 2 0 0 0-2-2h-8.59a2 2 0 0 0-1.41.59l-.2.21-4.8 8.8a2.2 2.2 0 0 0-.17 2.4" />
            </svg>
          </button>
        </div>
      ) : (
        <div className={styles.submittedFeedback}>
          <span className={styles.thankYou}>Thank you for your feedback!</span>
          <button 
            className={styles.editBtn}
            onClick={() => setSubmitted(false)}
          >
            Edit
          </button>
        </div>
      )}

      {showCommentInput && (
        <div className={styles.commentContainer}>
          <textarea
            className={styles.commentInput}
            value={comment}
            onChange={(e) => setComment(e.target.value)}
            placeholder="What was unhelpful about this response?"
            rows={3}
          />
          <div className={styles.commentActions}>
            <button 
              className={styles.cancelBtn} 
              onClick={handleCancel}
            >
              Cancel
            </button>
            <button 
              className={styles.submitBtn} 
              onClick={handleSubmitComment}
            >
              Submit
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default MessageFeedback; 