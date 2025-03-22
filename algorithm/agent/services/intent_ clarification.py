# file: app/services/intent_clarification.py
from typing import Dict, Any, List, Optional, Tuple
from agent.services.intent_classification import IntentType, IntentClassifier
import os
import json
import requests

class IntentClarifier:
    """Service for handling low-confidence intent classifications"""
    
    def __init__(self):
        self.api_key = os.environ.get("OPENAI_API_KEY")
        self.model = "gpt-4o"  # Or another appropriate model
        self.api_url = "https://api.openai.com/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        self.intent_classifier = IntentClassifier()
    
    async def generate_clarification_questions(self, 
                                              user_query: str, 
                                              original_intent: IntentType,
                                              confidence_assessment: Dict[str, Any],
                                              possible_intents: List[IntentType] = None) -> Dict[str, Any]:
        """
        Generate clarification questions for low-confidence intents
        
        Args:
            user_query: Original user query
            original_intent: Initially classified intent
            confidence_assessment: Confidence assessment details
            possible_intents: List of possible alternative intents
            
        Returns:
            Dict containing clarification questions and options
        """
        # If no alternatives provided, use top intents excluding the original
        if not possible_intents:
            all_intents = list(IntentType)
            all_intents.remove(IntentType.UNKNOWN)  # Don't suggest UNKNOWN as alternative
            if original_intent in all_intents:
                all_intents.remove(original_intent)
            possible_intents = all_intents[:2]  # Take top 2 alternatives
        
        # Prepare the prompt for the LLM
        system_prompt = """
        You are an assistant helping to clarify user intent on a job matching platform.
        The system is unsure about what the user wants to do. Generate a friendly message
        asking for clarification, along with 2-3 specific questions that will help determine
        their intent. Make the questions clear and directly related to the possible intents.
        
        Format your response as JSON with the following structure:
        {
            "clarification_message": "A friendly message explaining we need more information",
            "questions": [
                {
                    "question": "Clear, specific question text",
                    "intent_mapping": {
                        "answer_pattern_1": "corresponding_intent",
                        "answer_pattern_2": "different_intent"
                    }
                }
            ],
            "quick_options": [
                {
                    "text": "Option text (keep it short)",
                    "intent": "corresponding_intent"
                }
            ]
        }
        """
        
        # Get intent descriptions for context
        intent_examples = await self.intent_classifier.get_intent_examples()
        
        # Format intent information for the prompt
        intent_info = []
        for intent in [original_intent] + possible_intents:
            examples = intent_examples.get(intent, [])
            intent_info.append({
                "intent": intent,
                "examples": examples[:3]  # Limit to 3 examples per intent
            })
        
        user_prompt = f"""
        Original user query: "{user_query}"
        
        System's current best guess: {original_intent}
        Confidence level: {confidence_assessment['confidence_level']}
        
        Possible intents:
        {json.dumps(intent_info, indent=2)}
        
        Generate clarification questions and quick selection options to help determine if the user wants to:
        1. {original_intent}
        {', '.join([f"{i+2}. {intent}" for i, intent in enumerate(possible_intents)])}
        """
        
        try:
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json={
                    "model": self.model,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    "response_format": {"type": "json_object"}
                }
            )
            
            if response.status_code != 200:
                print(f"LLM API error: {response.text}")
                return self._get_fallback_clarification(original_intent, possible_intents)
            
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            
            # Parse the JSON response
            clarification = json.loads(content)
            
            # Add the original intent and possible alternatives to the response
            clarification["original_intent"] = original_intent
            clarification["possible_intents"] = possible_intents
            
            return clarification
            
        except Exception as e:
            print(f"Clarification generation error: {str(e)}")
            return self._get_fallback_clarification(original_intent, possible_intents)
    
    def _get_fallback_clarification(self, 
                                   original_intent: IntentType, 
                                   possible_intents: List[IntentType]) -> Dict[str, Any]:
        """
        Generate a fallback clarification if the LLM call fails
        
        Args:
            original_intent: Initially classified intent
            possible_intents: List of possible alternative intents
            
        Returns:
            Dict containing basic clarification options
        """
        intent_display_names = {
            IntentType.RESUME_ANALYSIS: "Analyze your resume",
            IntentType.JOB_MATCHING: "Find matching jobs",
            IntentType.RESUME_EDITING: "Improve your resume",
            IntentType.JOB_POSTING: "Post a job",
            IntentType.CANDIDATE_SEARCH: "Search for candidates",
            IntentType.UNKNOWN: "Something else"
        }
        
        quick_options = []
        quick_options.append({
            "text": intent_display_names.get(original_intent, str(original_intent)),
            "intent": original_intent
        })
        
        for intent in possible_intents:
            quick_options.append({
                "text": intent_display_names.get(intent, str(intent)),
                "intent": intent
            })
        
        return {
            "clarification_message": "I'm not quite sure what you're looking to do. Could you please clarify?",
            "questions": [
                {
                    "question": "What would you like to accomplish today?",
                    "intent_mapping": {
                        "resume|cv|analyze": IntentType.RESUME_ANALYSIS,
                        "match|find job": IntentType.JOB_MATCHING,
                        "improve|edit|update resume": IntentType.RESUME_EDITING,
                        "post|create|new job": IntentType.JOB_POSTING,
                        "candidate|applicant|search": IntentType.CANDIDATE_SEARCH
                    }
                }
            ],
            "quick_options": quick_options,
            "original_intent": original_intent,
            "possible_intents": possible_intents
        }
    
    async def process_clarification_response(self,
                                           original_query: str,
                                           clarification_response: str,
                                           clarification_context: Dict[str, Any]) -> Tuple[IntentType, float, Dict[str, Any]]:
        """
        Process user response to clarification questions
        
        Args:
            original_query: Original user query
            clarification_response: User's response to clarification
            clarification_context: Context from the clarification process
            
        Returns:
            Tuple of (IntentType, confidence_score, extracted_info)
        """
        # Check if the response matches any quick options
        quick_options = clarification_context.get("quick_options", [])
        for option in quick_options:
            option_text = option.get("text", "").lower()
            if option_text in clarification_response.lower():
                return IntentType(option.get("intent", IntentType.UNKNOWN)), 0.9, {}
        
        # Check if response matches any intent mappings in questions
        questions = clarification_context.get("questions", [])
        for question in questions:
            intent_mapping = question.get("intent_mapping", {})
            for pattern, intent in intent_mapping.items():
                if pattern.lower() in clarification_response.lower():
                    return IntentType(intent), 0.85, {}
        
        # If no match, combine the original query with clarification response
        # and reclassify with the intent classifier
        combined_query = f"{original_query} {clarification_response}"
        return await self.intent_classifier.classify_intent(combined_query)