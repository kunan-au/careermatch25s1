import sys
import os
import asyncio
import json
import time
from pathlib import Path
import statistics
from typing import Dict, List, Any
import re
import pytest
from dotenv import load_dotenv

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import entity extraction without mocking
from services.entity_extraction import EntityExtractor, EntityType, MetadataGenerator

# Load environment variables (for API keys)
load_dotenv()

# Test data
test_job_descriptions = [
    """
    Software Engineer (Backend)
    
    Company: TechCorp
    Location: San Francisco, CA (Remote option available)
    
    Job Description:
    We are looking for a talented Backend Software Engineer to join our growing team. The ideal candidate will have strong experience with Python, Django, and AWS cloud services.
    
    Responsibilities:
    - Design, develop, and maintain scalable backend services and APIs
    - Collaborate with frontend engineers to integrate user-facing elements
    - Optimize application performance and ensure high availability
    - Implement security and data protection measures
    
    Requirements:
    - 3+ years of experience in backend development
    - Proficiency in Python and Django framework
    - Experience with AWS services (Lambda, EC2, S3)
    - Knowledge of database systems (SQL and NoSQL)
    - Bachelor's degree in Computer Science or related field
    
    Preferred Qualifications:
    - Experience with Docker and Kubernetes
    - Knowledge of CI/CD pipelines
    - Familiarity with microservices architecture
    
    Salary: $120,000 - $150,000 per year
    """,
    
    """
    Data Scientist - Machine Learning
    
    Location: New York, NY
    
    About the Role:
    Join our data science team to develop and implement machine learning models that drive business decisions and product features.
    
    Key Responsibilities:
    - Build and deploy machine learning models for various business applications
    - Work with large datasets to extract insights and patterns
    - Collaborate with product and engineering teams
    - Present findings to non-technical stakeholders
    
    Required Skills:
    - 2-5 years of experience in data science or related field
    - Strong programming skills in Python
    - Experience with machine learning libraries (TensorFlow, PyTorch, scikit-learn)
    - MS or PhD in Computer Science, Statistics, or related field
    - Experience with SQL and data visualization tools
    
    Compensation: $130,000 - $160,000 annually
    """
]

# Ground truth for validation
ground_truth = {
    "job_descriptions": [
        {
            "skills": ["python", "django", "aws", "sql", "nosql", "docker", "kubernetes"],
            "job_titles": ["software engineer", "backend software engineer"],
            "locations": ["san francisco", "remote"],
            "experience": [{"min_years": 3}],
            "education": ["bachelor's degree"]
        },
        {
            "skills": ["python", "tensorflow", "pytorch", "scikit-learn", "sql"],
            "job_titles": ["data scientist"],
            "locations": ["new york"],
            "experience": [{"min_years": 2, "max_years": 5}],
            "education": ["ms", "phd"]
        }
    ]
}

@pytest.mark.asyncio
async def test_entity_extraction_with_real_api():
    """Test entity extraction functionality with real OpenAI API"""
    print("\n=== Entity Extraction Testing with Real OpenAI API ===\n")
    
    # Check if API key is available
    if not os.getenv("OPENAI_API_KEY"):
        pytest.skip("OPENAI_API_KEY environment variable not set")
    
    # Initialize the entity extractor
    extractor = EntityExtractor()
    
    # Set up metrics tracking
    metrics = {
        "processing_times": [],
        "precision": {"skill": [], "job_title": [], "location": [], "experience": [], "education": []},
        "recall": {"skill": [], "job_title": [], "location": [], "experience": [], "education": []}
    }
    
    # Test job descriptions
    print("Testing job descriptions with real OpenAI API...")
    for i, job_desc in enumerate(test_job_descriptions):
        print(f"\nProcessing job description {i+1}...")
        
        # Track processing time
        start_time = time.time()
        entities = await extractor.extract_entities(job_desc)
        processing_time = time.time() - start_time
        metrics["processing_times"].append(processing_time)
        
        print(f"Processing completed in {processing_time:.3f} seconds")
        print(f"Extracted entities: {json.dumps(entities, indent=2, default=str)}")
        
        # Calculate precision and recall for each entity type
        ground_truth_entities = ground_truth["job_descriptions"][i]
        
        # Skills
        extracted_skills = [s["text"].lower() for s in entities.get(EntityType.SKILL, [])]
        true_skills = ground_truth_entities["skills"]
        
        print(f"Extracted skills: {extracted_skills}")
        print(f"Expected skills: {true_skills}")
        
        metrics["precision"]["skill"].append(calculate_precision(extracted_skills, true_skills))
        metrics["recall"]["skill"].append(calculate_recall(extracted_skills, true_skills))
        
        # Job titles
        extracted_titles = [t["text"].lower() for t in entities.get(EntityType.JOB_TITLE, [])]
        true_titles = ground_truth_entities["job_titles"]
        
        print(f"Extracted job titles: {extracted_titles}")
        print(f"Expected job titles: {true_titles}")
        
        metrics["precision"]["job_title"].append(calculate_precision(extracted_titles, true_titles))
        metrics["recall"]["job_title"].append(calculate_recall(extracted_titles, true_titles))
        
        # Locations
        extracted_locations = [l["text"].lower() for l in entities.get(EntityType.LOCATION, [])]
        true_locations = ground_truth_entities["locations"]
        
        print(f"Extracted locations: {extracted_locations}")
        print(f"Expected locations: {true_locations}")
        
        metrics["precision"]["location"].append(calculate_precision(extracted_locations, true_locations))
        metrics["recall"]["location"].append(calculate_recall(extracted_locations, true_locations))
        
        # Verify JSON structure
        verify_json_structure(entities)
        
        # Verify relationships if available
        print("\nExtracting entity relationships...")
        relationships = await extractor.infer_entity_relationships(entities)
        print(f"Extracted relationships: {json.dumps(relationships, indent=2, default=str)}")
        verify_relationships(relationships, entities)
        
        # Extract structured information
        print("\nExtracting structured information...")
        structured_info = await extractor.extract_structured_info(job_desc)
        print(f"Structured information: {json.dumps(structured_info, indent=2, default=str)}")
    
    # Calculate aggregated metrics
    avg_processing_time = statistics.mean(metrics["processing_times"])
    
    avg_precision = {}
    avg_recall = {}
    for entity_type in metrics["precision"]:
        if metrics["precision"][entity_type]:
            avg_precision[entity_type] = statistics.mean(metrics["precision"][entity_type])
        if metrics["recall"][entity_type]:
            avg_recall[entity_type] = statistics.mean(metrics["recall"][entity_type])
    
    overall_precision = statistics.mean([avg_precision[et] for et in avg_precision])
    overall_recall = statistics.mean([avg_recall[et] for et in avg_recall])
    f1_score = 2 * (overall_precision * overall_recall) / (overall_precision + overall_recall) if (overall_precision + overall_recall) > 0 else 0
    
    # Print summary
    print("\n=== Test Results ===")
    print(f"Average processing time: {avg_processing_time:.3f} seconds")
    print(f"Overall precision: {overall_precision:.2f}")
    print(f"Overall recall: {overall_recall:.2f}")
    print(f"F1 score: {f1_score:.2f}")
    
    print("\nEntity type metrics:")
    for entity_type in avg_precision:
        print(f"  {entity_type}:")
        print(f"    Precision: {avg_precision.get(entity_type, 0):.2f}")
        print(f"    Recall: {avg_recall.get(entity_type, 0):.2f}")
    
    # Check if all acceptance criteria are met
    print("\n=== Acceptance Criteria Verification ===")
    
    # Criteria 1: Entity extraction achieves >85% precision and recall
    precision_ok = overall_precision > 0.85
    recall_ok = overall_recall > 0.85
    print(f"✓ Precision > 85%: {precision_ok} ({overall_precision:.2f})")
    print(f"✓ Recall > 85%: {recall_ok} ({overall_recall:.2f})")
    
    # Criteria 2: Processing completes within 3 seconds
    timing_ok = avg_processing_time < 3.0
    print(f"✓ Processing under 3 seconds: {timing_ok} ({avg_processing_time:.3f}s)")
    
    # Overall result
    all_criteria_met = precision_ok and recall_ok and timing_ok
    print(f"\nAll acceptance criteria met: {'✓' if all_criteria_met else '✗'}")
    
    return all_criteria_met

def calculate_precision(extracted_items, true_items):
    """Calculate precision"""
    if not extracted_items:
        return 0.0
    
    # Count how many extracted items are in the ground truth
    correct = sum(1 for item in extracted_items if any(true_item in item or item in true_item for true_item in true_items))
    return correct / len(extracted_items)

def calculate_recall(extracted_items, true_items):
    """Calculate recall"""
    if not true_items:
        return 0.0
    
    # Count how many ground truth items were extracted
    found = sum(1 for true_item in true_items if any(true_item in item or item in true_item for item in extracted_items))
    return found / len(true_items)

def verify_json_structure(entities):
    """Verify the JSON structure of extracted entities"""
    # Check that all entity types have the expected structure
    structure_valid = True
    
    for entity_type, entity_list in entities.items():
        if not isinstance(entity_list, list):
            print(f"Error: {entity_type} is not a list")
            structure_valid = False
            continue
        
        for entity in entity_list:
            if not isinstance(entity, dict):
                print(f"Error: Entity in {entity_type} is not a dictionary")
                structure_valid = False
                continue
            
            if "text" not in entity:
                print(f"Error: Entity in {entity_type} is missing 'text' field")
                structure_valid = False
    
    print(f"JSON structure validation: {'✓' if structure_valid else '✗'}")
    return structure_valid

def verify_relationships(relationships, entities):
    """Verify relationships between entities"""
    if not relationships:
        print("No relationships found")
        return False
    
    relationship_valid = True
    
    # Check skill-job relationships if available
    if "skill_job_relationships" in relationships:
        skill_job_rels = relationships["skill_job_relationships"]
        
        if not isinstance(skill_job_rels, list):
            print("Error: skill_job_relationships is not a list")
            relationship_valid = False
        else:
            for rel in skill_job_rels:
                if "job_title" not in rel or "related_skills" not in rel:
                    print("Error: Job-skill relationship missing required fields")
                    relationship_valid = False
                    continue
    
    # Check experience-skill relationships if available
    if "experience_skill_relationships" in relationships:
        exp_skill_rels = relationships["experience_skill_relationships"]
        
        if not isinstance(exp_skill_rels, list):
            print("Error: experience_skill_relationships is not a list")
            relationship_valid = False
    
    print(f"Relationship validation: {'✓' if relationship_valid else '✗'}")
    return relationship_valid
 
async def main():
    """Run entity extraction tests with real API"""
    # Make sure environment variables are loaded
    load_dotenv()
    
    # Check if API key is available
    if not os.getenv("OPENAI_API_KEY"):
        print("ERROR: OPENAI_API_KEY environment variable not set.")
        print("Please set your OpenAI API key in the .env file or environment.")
        sys.exit(1)
    
    # Run tests
    success = await test_entity_extraction_with_real_api()
    
    print("\nTest execution completed.")
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    asyncio.run(main())