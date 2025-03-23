from typing import Dict, Any, List, Optional, Tuple
import os
import json
import requests
import re
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class EntityType(str, Enum):
    SKILL = "skill"
    JOB_TITLE = "job_title"
    LOCATION = "location"
    SALARY = "salary"
    EXPERIENCE = "experience"
    EDUCATION = "education"
    COMPANY = "company"
    DATE = "date"
    OTHER = "other"

class EntityExtractor:
    """Service for extracting entities from text"""
    
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model = "gpt-4o-mini"
        self.api_url = "https://api.openai.com/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # Load skills taxonomy (simplified for this example)
        self._load_skills_taxonomy()
        
        # Common job titles for pattern recognition
        self._load_job_titles()
        
        # Location patterns (cities, states, countries)
        self._load_locations()
    
    def _load_skills_taxonomy(self):
        """Load skills taxonomy for pattern matching"""
        # In a real implementation, this would load from a database or file
        # For this example, we'll use a small sample
        self.skills = [
            "python", "javascript", "java", "c++", "ruby", "golang", "typescript",
            "react", "angular", "vue", "node.js", "express", "django", "flask",
            "aws", "azure", "gcp", "docker", "kubernetes", "terraform",
            "machine learning", "ai", "data science", "nlp", "computer vision",
            "sql", "mongodb", "postgresql", "mysql", "oracle", "redis",
            "agile", "scrum", "kanban", "product management", "jira", "confluence",
            "figma", "sketch", "photoshop", "illustrator", "ui/ux", "design thinking"
        ]
    
    def _load_job_titles(self):
        """Load common job titles for pattern matching"""
        # In a real implementation, this would load from a database or file
        self.job_titles = [
            "software engineer", "software developer", "full stack developer", "frontend developer",
            "backend developer", "devops engineer", "site reliability engineer", "data scientist",
            "data analyst", "data engineer", "machine learning engineer", "ai researcher",
            "product manager", "project manager", "scrum master", "product owner",
            "ux designer", "ui designer", "graphic designer", "web designer",
            "marketing manager", "digital marketing specialist", "content writer",
            "human resources", "hr manager", "recruiter", "talent acquisition"
        ]
    
    def _load_locations(self):
        """Load location patterns"""
        # In a real implementation, this would load from a database or file
        self.locations = [
            "san francisco", "new york", "chicago", "austin", "seattle", "los angeles",
            "boston", "denver", "atlanta", "miami", "washington dc", "portland",
            "california", "texas", "new york", "florida", "massachusetts", "washington",
            "remote", "hybrid", "onsite", "usa", "canada", "uk", "germany", "india"
        ]
    
    async def extract_entities(self, text: str, entity_types: Optional[List[EntityType]] = None) -> Dict[str, List[Dict[str, Any]]]:
        """
        Extract entities from text
        
        Args:
            text: Text to extract entities from
            entity_types: Optional list of entity types to extract
            
        Returns:
            Dict mapping entity types to lists of extracted entities
        """
        # If no specific entity types requested, extract all
        if not entity_types:
            entity_types = [et for et in EntityType]
        
        # Initialize results
        results = {et: [] for et in entity_types}
        
        # First use pattern matching for faster extraction of common entities
        self._extract_entities_by_pattern(text, results)
        
        # For complex entities or when pattern matching yields few results, 
        # use LLM-based extraction
        if (len(results[EntityType.SKILL]) < 3 or 
            len(results[EntityType.JOB_TITLE]) < 1 or
            EntityType.EXPERIENCE in entity_types or 
            EntityType.EDUCATION in entity_types or
            EntityType.SALARY in entity_types):
            
            await self._extract_entities_with_llm(text, entity_types, results)
        
        return results
    
    def _extract_entities_by_pattern(self, text: str, results: Dict[str, List[Dict[str, Any]]]):
        """
        Extract entities using pattern matching
        
        Args:
            text: Text to extract from
            results: Results dictionary to populate
        """
        text_lower = text.lower()
        
        # Extract skills
        if EntityType.SKILL in results:
            for skill in self.skills:
                if re.search(r'\b' + re.escape(skill) + r'\b', text_lower):
                    results[EntityType.SKILL].append({
                        "text": skill,
                        "source": "pattern",
                        "confidence": 0.9
                    })
        
        # Extract job titles
        if EntityType.JOB_TITLE in results:
            for title in self.job_titles:
                if re.search(r'\b' + re.escape(title) + r'\b', text_lower):
                    results[EntityType.JOB_TITLE].append({
                        "text": title,
                        "source": "pattern",
                        "confidence": 0.85
                    })
        
        # Extract locations
        if EntityType.LOCATION in results:
            for location in self.locations:
                if re.search(r'\b' + re.escape(location) + r'\b', text_lower):
                    results[EntityType.LOCATION].append({
                        "text": location,
                        "source": "pattern",
                        "confidence": 0.8
                    })
        
        # Extract salary using regex patterns
        if EntityType.SALARY in results:
            # Patterns for different salary formats
            salary_patterns = [
                r'\$(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)(?:\s*-\s*\$(\d{1,3}(?:,\d{3})*(?:\.\d{2})?))?\s*(?:per|\/|a)\s*(?:year|yr|annual|annum|annually)',
                r'(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)\s*k(?:\s*-\s*(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)\s*k)?',
                r'(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)(?:\s*-\s*(\d{1,3}(?:,\d{3})*(?:\.\d{2})?))?\s*(?:USD|EUR|GBP)'
            ]
            
            for pattern in salary_patterns:
                matches = re.finditer(pattern, text, re.IGNORECASE)
                for match in matches:
                    min_salary = match.group(1).replace(',', '') if match.group(1) else None
                    max_salary = match.group(2).replace(',', '') if match.group(2) else None
                    
                    # For k notation, multiply by 1000
                    if 'k' in pattern:
                        if min_salary:
                            min_salary = str(float(min_salary) * 1000)
                        if max_salary:
                            max_salary = str(float(max_salary) * 1000)
                    
                    salary_info = {
                        "text": match.group(0),
                        "min_salary": min_salary,
                        "max_salary": max_salary,
                        "currency": "USD",  # Default, improve with regex for specific currencies
                        "source": "pattern",
                        "confidence": 0.75
                    }
                    
                    results[EntityType.SALARY].append(salary_info)
        
        # Date extraction
        if EntityType.DATE in results:
            date_patterns = [
                r'\b(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+\d{1,2},?\s+\d{4}\b',
                r'\b\d{1,2}/\d{1,2}/\d{2,4}\b',
                r'\b\d{4}-\d{1,2}-\d{1,2}\b'
            ]
            
            for pattern in date_patterns:
                matches = re.finditer(pattern, text, re.IGNORECASE)
                for match in matches:
                    date_info = {
                        "text": match.group(0),
                        "source": "pattern",
                        "confidence": 0.8
                    }
                    results[EntityType.DATE].append(date_info)
    
    async def _extract_entities_with_llm(self, 
                                       text: str, 
                                       entity_types: List[EntityType], 
                                       results: Dict[str, List[Dict[str, Any]]]):
        """
        Extract entities using LLM for more complex extraction
        
        Args:
            text: Text to extract from
            entity_types: List of entity types to extract
            results: Results dictionary to update
        """
        # Prepare the prompt for the LLM
        entity_descriptions = {
            EntityType.SKILL: "Technical skills, programming languages, tools, frameworks, or soft skills",
            EntityType.JOB_TITLE: "Job positions or roles",
            EntityType.LOCATION: "Geographical locations, cities, countries, or work arrangements (remote, hybrid)",
            EntityType.SALARY: "Salary information including amounts, ranges, and currency",
            EntityType.EXPERIENCE: "Work experience requirements, years of experience",
            EntityType.EDUCATION: "Educational requirements, degrees, certifications",
            EntityType.COMPANY: "Company or organization names",
            EntityType.DATE: "Dates mentioned in the text"
        }
        
        entity_list = []
        for entity in entity_types:
            if entity in entity_descriptions:
                entity_list.append(f"- {entity}: {entity_descriptions[entity]}")
        
        entities_to_extract = "\n".join(entity_list)
        
        system_prompt = f"""
        You are an expert entity extraction system for job-related text. Extract the following entity types from the provided text:
        
        {entities_to_extract}
        
        Format your response as a JSON object where each key is an entity type, and the value is an array of objects with:
        - "text": the extracted text
        - "normalized_text": a standardized version of the text (where applicable)
        - Additional entity-specific fields as needed
        
        For example, for skill entities, include a "category" field if possible.
        For salary entities, include "min_salary", "max_salary", and "currency" if available.
        For experience, include "min_years" and "max_years" if specified.
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
                        {"role": "user", "content": f"Extract entities from this text:\n\n{text}"}
                    ],
                    "response_format": {"type": "json_object"}
                }
            )
            
            if response.status_code != 200:
                logger.error(f"LLM API error: {response.text}")
                return
            
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            
            # Parse the JSON response
            extracted_entities = json.loads(content)
            
            # Update our results dictionary with LLM results
            for entity_type, entities in extracted_entities.items():
                if entity_type in results and isinstance(entities, list):
                    # Mark these entities as coming from LLM
                    for entity in entities:
                        entity["source"] = "llm"
                        entity["confidence"] = 0.8  # Default confidence for LLM extractions
                        
                    # Add to results, avoiding duplicates
                    existing_texts = {e["text"].lower() for e in results[entity_type]}
                    for entity in entities:
                        if entity["text"].lower() not in existing_texts:
                            results[entity_type].append(entity)
                            existing_texts.add(entity["text"].lower())
            
        except Exception as e:
            logger.error(f"Entity extraction with LLM error: {str(e)}")
    
    async def extract_structured_info(self, text: str) -> Dict[str, Any]:
        """
        Extract structured information like experience, education, requirements
        
        Args:
            text: Text to extract from (e.g., job description or resume)
            
        Returns:
            Dict with structured information
        """
        system_prompt = """
        You are an expert at extracting structured information from job-related text. Extract the following information in a structured format:
        
        For job descriptions:
        - Job responsibilities/duties (as a list)
        - Required qualifications (as a list)
        - Preferred qualifications (as a list)
        - Benefits (as a list)
        - Company description (as text)
        
        For resumes:
        - Work experience (as a list of positions with company, title, dates, and descriptions)
        - Education (as a list of degrees with institution, dates, and fields of study)
        - Projects (as a list with names and descriptions)
        - Certifications (as a list)
        
        Format your response as a JSON object.
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
                        {"role": "user", "content": f"Extract structured information from this text:\n\n{text}"}
                    ],
                    "response_format": {"type": "json_object"}
                }
            )
            
            if response.status_code != 200:
                logger.error(f"LLM API error: {response.text}")
                return {}
            
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            
            # Parse the JSON response
            structured_info = json.loads(content)
            return structured_info
            
        except Exception as e:
            logger.error(f"Structured info extraction error: {str(e)}")
            return {}
    
    async def infer_entity_relationships(self, entities: Dict[str, List[Dict[str, Any]]]) -> Dict[str, List[Dict[str, Any]]]:
        """
        Infer relationships between extracted entities
        
        Args:
            entities: Dictionary of extracted entities
            
        Returns:
            Dict with relationship information
        """
        relationships = {}
        
        # Skill-Job Title relationships (which skills are related to which job titles)
        if EntityType.SKILL in entities and EntityType.JOB_TITLE in entities:
            skill_job_rels = []
            
            for job in entities[EntityType.JOB_TITLE]:
                related_skills = []
                
                for skill in entities[EntityType.SKILL]:
                    # In a real implementation, we'd use a knowledge graph or ML model
                    # For this example, we'll use a simplified approach
                    relevance_score = 0.5  # Default medium relevance
                    
                    # Add skill-job relationship
                    related_skills.append({
                        "skill": skill["text"],
                        "relevance": relevance_score
                    })
                
                skill_job_rels.append({
                    "job_title": job["text"],
                    "related_skills": related_skills
                })
            
            relationships["skill_job_relationships"] = skill_job_rels
        
        # Experience-Skill relationships
        if EntityType.EXPERIENCE in entities and EntityType.SKILL in entities:
            # Simple mapping of experience levels to skills
            exp_skill_rels = []
            
            for exp in entities[EntityType.EXPERIENCE]:
                min_years = exp.get("min_years", 0)
                
                # Simple categorization of skills by experience level
                junior_skills = []
                mid_skills = []
                senior_skills = []
                
                for skill in entities[EntityType.SKILL]:
                    # Simplified logic - in real app would use a knowledge base
                    if min_years < 2:
                        junior_skills.append(skill["text"])
                    elif min_years < 5:
                        mid_skills.append(skill["text"])
                    else:
                        senior_skills.append(skill["text"])
                
                exp_skill_rels.append({
                    "experience_level": f"{min_years}+ years",
                    "junior_skills": junior_skills,
                    "mid_level_skills": mid_skills,
                    "senior_skills": senior_skills
                })
            
            relationships["experience_skill_relationships"] = exp_skill_rels
        
        return relationships

class MetadataGenerator:
    """Generate metadata tags and categories from entities"""
    
    def __init__(self):
        # Initialize category mappings
        self._init_category_mappings()
        self._init_industry_mappings()
    
    def _init_category_mappings(self):
        """Initialize job category mappings"""
        self.category_mappings = {
            # Tech categories
            "software": ["software engineer", "software developer", "full stack", "frontend", "backend"],
            "data": ["data scientist", "data analyst", "data engineer", "machine learning", "ai", "analytics"],
            "devops": ["devops", "sre", "site reliability", "infrastructure", "cloud", "aws", "azure", "gcp"],
            "design": ["designer", "ux", "ui", "user experience", "user interface", "graphic"],
            # Business categories
            "product": ["product manager", "product owner", "product lead"],
            "marketing": ["marketing", "seo", "social media", "content writer", "copywriter"],
            "sales": ["sales", "account executive", "business development"],
            "hr": ["hr", "human resources", "recruiter", "talent", "people"]
        }
    
    def _init_industry_mappings(self):
        """Initialize industry mappings"""
        self.industry_keywords = {
            "technology": ["tech", "software", "saas", "app", "platform", "startup"],
            "healthcare": ["health", "medical", "hospital", "patient", "clinic", "pharma"],
            "finance": ["finance", "bank", "investment", "fintech", "trading", "insurance"],
            "education": ["education", "learning", "teaching", "student", "school", "university"],
            "retail": ["retail", "e-commerce", "store", "consumer", "goods", "shopping"],
            "manufacturing": ["manufacturing", "production", "factory", "industrial", "assembly"],
            "media": ["media", "entertainment", "news", "publishing", "content", "creative"]
        }
        
    def _determine_categories(self, entities: Dict[str, List[Dict[str, Any]]]) -> List[str]:
        """
        Determine job categories based on job titles and skills
        
        Args:
            entities: Dictionary of extracted entities
            
        Returns:
            List of job categories
        """
        categories = set()
        
        # Match job titles to categories
        if EntityType.JOB_TITLE in entities:
            for job in entities[EntityType.JOB_TITLE]:
                job_title = job["text"].lower()
                
                for category, keywords in self.category_mappings.items():
                    if any(keyword in job_title for keyword in keywords):
                        categories.add(category)
        
        # If no categories found from job titles, try with skills
        if not categories and EntityType.SKILL in entities:
            tech_skills = ["python", "java", "javascript", "react", "angular", "vue", "node", "aws", "azure"]
            data_skills = ["sql", "python", "r", "pandas", "numpy", "tensorflow", "pytorch", "tableau"]
            design_skills = ["figma", "sketch", "photoshop", "illustrator", "ui", "ux"]
            
            skill_texts = [skill["text"].lower() for skill in entities[EntityType.SKILL]]
            
            if any(skill in skill_texts for skill in tech_skills):
                categories.add("software")
            
            if any(skill in skill_texts for skill in data_skills):
                categories.add("data")
            
            if any(skill in skill_texts for skill in design_skills):
                categories.add("design")
        
        return list(categories)
    
    def _determine_seniority(self, entities: Dict[str, List[Dict[str, Any]]], text_content: str) -> str:
        """
        Determine seniority level based on entities and text content
        
        Args:
            entities: Dictionary of extracted entities
            text_content: Original text content
            
        Returns:
            Seniority level as string
        """
        text_lower = text_content.lower()
        
        # Look for explicit seniority indicators in job titles
        if EntityType.JOB_TITLE in entities:
            for job in entities[EntityType.JOB_TITLE]:
                job_title = job["text"].lower()
                
                if any(word in job_title for word in ["senior", "sr", "lead", "principal", "staff"]):
                    return "senior"
                elif any(word in job_title for word in ["junior", "jr", "associate", "entry"]):
                    return "junior"
                elif any(word in job_title for word in ["manager", "director", "head"]):
                    return "manager"
        
        # Look for experience requirements
        if EntityType.EXPERIENCE in entities:
            for exp in entities[EntityType.EXPERIENCE]:
                min_years = exp.get("min_years", 0)
                
                if min_years >= 5:
                    return "senior"
                elif min_years >= 2:
                    return "mid"
                else:
                    return "junior"
        
        # Scan the text for seniority indicators
        senior_indicators = ["senior", "experienced", "expert", "lead", "5+ years", "advanced"]
        junior_indicators = ["junior", "entry", "beginner", "0-2 years", "graduate", "recent"]
        manager_indicators = ["manager", "management", "head of", "director", "leadership"]
        
        if any(indicator in text_lower for indicator in senior_indicators):
            return "senior"
        elif any(indicator in text_lower for indicator in manager_indicators):
            return "manager"
        elif any(indicator in text_lower for indicator in junior_indicators):
            return "junior"
        
        # Default to mid-level if no clear indicators
        return "mid"
    
    def _determine_industry(self, entities: Dict[str, List[Dict[str, Any]]], text_content: str) -> str:
        """
        Determine industry based on entities and text content
        
        Args:
            entities: Dictionary of extracted entities
            text_content: Original text content
            
        Returns:
            Industry as string
        """
        text_lower = text_content.lower()
        
        # Check company entities first
        if EntityType.COMPANY in entities:
            for company in entities[EntityType.COMPANY]:
                company_name = company["text"].lower()
                
                # Known companies and their industries (simplified)
                known_companies = {
                    "google": "technology",
                    "amazon": "technology",
                    "apple": "technology",
                    "microsoft": "technology",
                    "meta": "technology",
                    "facebook": "technology",
                    "walmart": "retail",
                    "target": "retail",
                    "jpmorgan": "finance",
                    "goldman sachs": "finance",
                    "bank of america": "finance",
                    "pfizer": "healthcare",
                    "johnson & johnson": "healthcare"
                }
                
                for known_company, industry in known_companies.items():
                    if known_company in company_name:
                        return industry
        
        # Scan the text for industry keywords
        for industry, keywords in self.industry_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                return industry
        
        # If still unknown, default to None
        return None
    
    def _determine_job_type(self, entities: Dict[str, List[Dict[str, Any]]], text_content: str) -> str:
        """
        Determine job type (full-time, part-time, contract, etc.)
        
        Args:
            entities: Dictionary of extracted entities
            text_content: Original text content
            
        Returns:
            Job type as string
        """
        text_lower = text_content.lower()
        
        # Define job type patterns
        job_type_patterns = {
            "full-time": ["full time", "full-time", "permanent", "40 hours", "ft "],
            "part-time": ["part time", "part-time", "20 hours", "pt "],
            "contract": ["contract", "temporary", "contractor", "6 month", "3 month"],
            "freelance": ["freelance", "freelancer", "gig"],
            "internship": ["intern", "internship", "student"]
        }
        
        # Scan text for job type indicators
        for job_type, patterns in job_type_patterns.items():
            if any(pattern in text_lower for pattern in patterns):
                return job_type
        
        # Default to full-time if not specified
        return "full-time"
    
    def _determine_priority(self, entities: Dict[str, List[Dict[str, Any]]], text_content: str) -> str:
        """
        Determine priority tag (high, medium, low)
        
        Args:
            entities: Dictionary of extracted entities
            text_content: Original text content
            
        Returns:
            Priority as string
        """
        # Factors that might increase priority
        priority_signals = 0
        
        # Factor 1: Salary range (higher salary -> higher priority)
        if EntityType.SALARY in entities and entities[EntityType.SALARY]:
            salary = entities[EntityType.SALARY][0]
            # Parse out min salary and convert to number
            min_salary = salary.get("min_salary")
            if min_salary and float(min_salary) > 100000:
                priority_signals += 2
            elif min_salary and float(min_salary) > 80000:
                priority_signals += 1
        
        # Factor 2: In-demand skills
        if EntityType.SKILL in entities:
            in_demand_skills = ["machine learning", "data science", "blockchain", "react", "cloud", "aws", "ai"]
            skill_texts = [skill["text"].lower() for skill in entities[EntityType.SKILL]]
            
            if any(skill in skill_texts for skill in in_demand_skills):
                priority_signals += 1
        
        # Factor 3: Urgency indicators in text
        urgency_indicators = ["urgent", "immediate", "asap", "quickly", "fast", "priority"]
        if any(indicator in text_content.lower() for indicator in urgency_indicators):
            priority_signals += 1
        
        # Determine priority level based on signals
        if priority_signals >= 2:
            return "high"
        elif priority_signals == 1:
            return "medium"
        else:
            return "low"
    
    def generate_metadata(self, 
                         entities: Dict[str, List[Dict[str, Any]]], 
                         text_content: str) -> Dict[str, Any]:
        """
        Generate metadata from entities and text
        
        Args:
            entities: Extracted entities
            text_content: Original text content
            
        Returns:
            Dict with metadata
        """
        metadata = {
            "tags": [],
            "categories": [],
            "seniority_level": None,
            "industry": None,
            "job_type": None,
            "priority": "medium"
        }
        
        # Generate tags from skills
        if EntityType.SKILL in entities:
            for skill in entities[EntityType.SKILL]:
                if skill["text"] not in metadata["tags"]:
                    metadata["tags"].append(skill["text"])
        
        # Determine job categories from job titles and skills
        if EntityType.JOB_TITLE in entities:
            categories = self._determine_categories(entities)
            metadata["categories"] = categories
        
        # Determine seniority level
        metadata["seniority_level"] = self._determine_seniority(entities, text_content)
        
        # Determine industry
        metadata["industry"] = self._determine_industry(entities, text_content)
        
        # Determine job type
        metadata["job_type"] = self._determine_job_type(entities, text_content)
        
        # Determine priority based on several factors
        metadata["priority"] = self._determine_priority(entities, text_content)
        
        return metadata
    