# file: app/services/intent_confidence.py
from typing import Dict, Any, List, Tuple
from agent.services.intent_classification import IntentType
import logging

logger = logging.getLogger(__name__)

class IntentConfidenceScorer:
    """Service for assessing confidence in intent classifications"""
    
    def __init__(self):
        # Configurable thresholds
        self.high_confidence_threshold = 0.85
        self.medium_confidence_threshold = 0.60
        self.low_confidence_threshold = 0.40
    
    def assess_confidence(self, 
                          intent: IntentType, 
                          confidence_score: float, 
                          user_context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Assess the reliability of an intent classification
        
        Args:
            intent: The classified intent
            confidence_score: Raw confidence score from classifier
            user_context: User context for additional signals
            
        Returns:
            Dict containing confidence assessment
        """
        # Clamp confidence score to 0-1 range
        adjusted_score = max(0.0, min(1.0, confidence_score))
        
        # Apply context-based adjustments
        if user_context:
            adjusted_score = self._adjust_score_with_context(intent, adjusted_score, user_context)
        
        # Determine confidence level
        confidence_level = self._get_confidence_level(adjusted_score)
        
        # Log confidence assessment
        logger.info(f"Intent confidence assessment: {intent} with score {adjusted_score} -> {confidence_level}")
        
        return {
            "intent": intent,
            "raw_confidence": confidence_score,
            "adjusted_confidence": adjusted_score,
            "confidence_level": confidence_level,
            "is_reliable": confidence_level != "low"
        }
    
    def _adjust_score_with_context(self, 
                                   intent: IntentType, 
                                   score: float, 
                                   context: Dict[str, Any]) -> float:
        """
        Adjust confidence score based on user context
        
        Args:
            intent: The classified intent
            score: Raw confidence score
            context: User context
            
        Returns:
            Adjusted confidence score
        """
        adjusted_score = score
        
        # Adjust based on user type
        user_type = context.get("user_type")
        if user_type == "job_seeker" and intent in [IntentType.JOB_POSTING, IntentType.CANDIDATE_SEARCH]:
            # Job seekers rarely have these intents, reduce confidence
            adjusted_score *= 0.8
        elif user_type == "recruiter" and intent in [IntentType.RESUME_EDITING, IntentType.RESUME_ANALYSIS]:
            # Recruiters rarely have these intents, reduce confidence
            adjusted_score *= 0.8
        
        # Adjust based on recent actions
        recent_actions = context.get("recent_actions", [])
        for action in recent_actions:
            if action == "uploaded_resume" and intent == IntentType.RESUME_ANALYSIS:
                # If user just uploaded a resume, analysis intent is more likely
                adjusted_score = min(1.0, adjusted_score * 1.2)
            elif action == "viewed_jobs" and intent == IntentType.JOB_MATCHING:
                # If user was viewing jobs, matching intent is more likely
                adjusted_score = min(1.0, adjusted_score * 1.1)
        
        # Prevent adjusted score from going below a minimum threshold
        min_threshold = 0.1
        return max(min_threshold, adjusted_score)
    
    def _get_confidence_level(self, score: float) -> str:
        """
        Map confidence score to a categorical level
        
        Args:
            score: Confidence score (0-1)
            
        Returns:
            String confidence level ("high", "medium", or "low")
        """
        if score >= self.high_confidence_threshold:
            return "high"
        elif score >= self.medium_confidence_threshold:
            return "medium"
        elif score >= self.low_confidence_threshold:
            return "low"
        else:
            return "very_low"