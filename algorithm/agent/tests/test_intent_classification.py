# file: tests/test_intent_classification.py
import pytest
import asyncio
from ..services.intent_classification import IntentClassifier, IntentType

# Initialize the classifier
classifier = IntentClassifier()

# Test cases for intent classification
@pytest.mark.asyncio
async def test_resume_analysis_intent():
    """Test classification of resume analysis intent"""
    queries = [
        "Can you analyze my resume and provide feedback?",
        "What are the strengths and weaknesses of my resume?",
        "Please review my resume and suggest improvements.",
        "Does my resume meet the industry standards?",
        "Assess my resume for potential red flags."
    ]
    
    for query in queries:
        intent, confidence, _ = await classifier.classify_intent(query)
        
        # # for debugging 
        # print(f"Query: {query}")
        # print(f"LLM Response: {_}")
        # print(f"Predicted Intent: {intent}, Confidence: {confidence}")

        assert intent == IntentType.RESUME_ANALYSIS
        assert confidence > 0.7

@pytest.mark.asyncio
async def test_job_matching_intent():
    """Test classification of job matching intent"""
    queries = [
        "Find me jobs that match my resume",
        "What jobs am I qualified for?",
        "Show me job matches",
        "Are there any jobs for a Python developer?",
        "Match my skills to available positions"
    ]
    
    for query in queries:
        intent, confidence, _ = await classifier.classify_intent(query)
        assert intent == IntentType.JOB_MATCHING
        assert confidence > 0.7

@pytest.mark.asyncio
async def test_resume_editing_intent():
    """Test classification of resume editing intent"""
    queries = [
        "Help me edit my resume",
        "I need to update my work experience",
        "Can you add keywords to my resume?",
        "Format my resume for ATS systems",
        "Fix the formatting on my CV"
    ]
    
    for query in queries:
        intent, confidence, _ = await classifier.classify_intent(query)
        assert intent == IntentType.RESUME_EDITING
        assert confidence > 0.7

@pytest.mark.asyncio
async def test_job_posting_intent():
    """Test classification of job posting intent"""
    queries = [
        "I want to post a new job",
        "How do I create a job listing?",
        "Help me write a job description",
        "Post this job to your platform",
        "Create a new position for my company"
    ]

    
    
    for query in queries:
        intent, confidence, _ = await classifier.classify_intent(query)
        assert intent == IntentType.JOB_POSTING
        assert confidence > 0.7

@pytest.mark.asyncio
async def test_candidate_search_intent():
    """Test classification of candidate search intent"""
    queries = [
        "Find candidates with Python experience",
        "Search for developers in New York",
        "Show me applicants for my job posting",
        "I need to hire a marketing specialist",
        "Find qualified candidates for my open position"
    ]
    
    for query in queries:
        intent, confidence, _ = await classifier.classify_intent(query)
        assert intent == IntentType.CANDIDATE_SEARCH
        assert confidence > 0.7

@pytest.mark.asyncio
async def test_unknown_intent():
    """Test classification of unknown intent"""
    queries = [
        "What's the weather like today?",
        "Tell me a joke",
        "What time is it?",
        "How do I reset my password?",
        "Can you recommend a good restaurant?"
    ]
    
    for query in queries:
        intent, confidence, _ = await classifier.classify_intent(query)
        assert intent == IntentType.UNKNOWN or confidence < 0.4

@pytest.mark.asyncio
async def test_with_context():
    """Test intent classification with context information"""
    # Test with job seeker context
    job_seeker_context = {"user_type": "job_seeker", "recent_actions": ["uploaded_resume"]}
    query = "How does it look?"
    
    intent, confidence, _ = await classifier.classify_intent(query, job_seeker_context)
    assert intent == IntentType.RESUME_ANALYSIS
    
    # Test with recruiter context
    recruiter_context = {"user_type": "recruiter", "recent_actions": ["posted_job"]}
    query = "Find good matches"
    
    intent, confidence, _ = await classifier.classify_intent(query, recruiter_context)
    assert intent == IntentType.CANDIDATE_SEARCH