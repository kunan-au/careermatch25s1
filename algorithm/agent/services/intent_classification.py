from typing import Dict, Any, List, Tuple, Optional
import os
import json
import requests
from enum import Enum


class IntentType(str, Enum):
    RESUME_ANALYSIS = "resume_analysis"
    JOB_MATCHING = "job_matching"
    RESUME_EDITING = "resume_editing"
    JOB_POSTING = "job_posting"
    CANDIDATE_SEARCH = "candidate_search"
    UNKNOWN = "unknown"

# from dotenv import load_dotenv
# import os

# # load .env file
# load_dotenv()

# import json
# import os

# CACHE_FILE = "intent_cache.json"

# def load_cache():
#     if os.path.exists(CACHE_FILE):
#         with open(CACHE_FILE, "r") as f:
#             return json.load(f)
#     return {}

# def save_cache(cache):
#     with open(CACHE_FILE, "w") as f:
#         json.dump(cache, f)

# class IntentClassifier:
#     def __init__(self):
#         self.cache = load_cache()

#     async def classify_intent(self, user_query: str):
#         if user_query in self.cache:
#             return self.cache[user_query]
        
#         response = requests.post(self.api_url, headers=self.headers, json={"query": user_query})
#         result = response.json()
        
#         self.cache[user_query] = result
#         save_cache(self.cache)

#         return result
    

class IntentClassifier:
    """Service for classifying user intents using LLM"""
    
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model = "gpt-4o-mini"  # change model to gpt-4o-mini
        self.api_url = "https://api.openai.com/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    async def classify_intent(self, 
                              user_query: str, 
                              user_context: Optional[Dict[str, Any]] = None) -> Tuple[IntentType, float, Dict[str, Any]]:
        """
        Classify user intent from query and context
        
        Args:
            user_query: The user's query or request
            user_context: Additional context about the user (optional)
            
        Returns:
            Tuple containing:
            - IntentType: The classified intent
            - float: Confidence score (0-1)
            - Dict: Additional extracted information
        """
        if not user_query:
            return IntentType.UNKNOWN, 0.0, {}
        
        # Prepare context information if available
        context_str = ""
        if user_context:
            if user_context.get("user_type") == "job_seeker":
                context_str += "User is a job seeker. "
            elif user_context.get("user_type") == "recruiter":
                context_str += "User is a recruiter. "
            
            if user_context.get("recent_actions"):
                context_str += f"Recent actions: {', '.join(user_context['recent_actions'])}. "
        
        # Prepare the prompt for the LLM
        system_prompt = """
        You are an intent classification system for a job matching platform. 
        Your task is to determine the user's intent from their query and any provided context.
        
        Possible intents:
        1. resume_analysis - User wants to analyze or evaluate their resume (e.g., review, strengths, weaknesses, industry standards).
        2. job_matching - User wants to find matching jobs for their profile (e.g., formatting, adding keywords, fixing errors).
        3. resume_editing - User wants to modify or improve their resume
        4. job_posting - User wants to post or manage a job listing
        5. candidate_search - User wants to find candidates for a job
        6. unknown - The intent is unclear or not related to the above categories
        
        Provide your classification in JSON format with the following fields:
        - intent: The classified intent (one of the above)
        - confidence: Your confidence score from 0 to 1
        - extracted_info: Any relevant information extracted from the query
        """
        
        # Call the LLM
        try:
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json={
                    "model": self.model,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": f"User query: {user_query}\nContext: {context_str}"}
                    ],
                    "response_format": {"type": "json_object"}
                }
            )
            
            if response.status_code != 200:
                print(f"LLM API error: {response.text}")
                return IntentType.UNKNOWN, 0.0, {}
            
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            
            # Parse the JSON response
            classification = json.loads(content)
            
            intent = IntentType(classification.get("intent", IntentType.UNKNOWN))
            confidence = float(classification.get("confidence", 0.0))
            extracted_info = classification.get("extracted_info", {})
            
            return intent, confidence, extracted_info
            
        except Exception as e:
            print(f"Intent classification error: {str(e)}")
            return IntentType.UNKNOWN, 0.0, {}
    
    async def get_intent_examples(self) -> Dict[IntentType, List[str]]:
        """
        Get example queries for each intent type
        Used for training and documentation
        """
        return {
            IntentType.RESUME_ANALYSIS: [
                "Can you analyze my resume?",
                "How good is my CV?",
                "What's wrong with my resume?",
                "Review my resume for mistakes",
                "Is my resume ATS friendly?"
            ],
            IntentType.JOB_MATCHING: [
                "Find jobs that match my profile",
                "What jobs am I qualified for?",
                "Show me jobs that fit my skills",
                "Match my resume to open positions",
                "Are there any good jobs for me?"
            ],
            IntentType.RESUME_EDITING: [
                "Help me improve my resume",
                "Fix my resume format",
                "I need to update my work experience",
                "Make my resume better for tech jobs",
                "Add keywords to my resume"
            ],
            IntentType.JOB_POSTING: [
                "I want to post a new job",
                "How do I create a job listing?",
                "Edit my job posting",
                "Update the requirements for my job listing",
                "Duplicate my previous job posting"
            ],
            IntentType.CANDIDATE_SEARCH: [
                "Find candidates with JavaScript experience",
                "Search for developers in New York",
                "Show me applicants for the marketing position",
                "Filter candidates by education level",
                "Who's the best match for my job?"
            ]
        }