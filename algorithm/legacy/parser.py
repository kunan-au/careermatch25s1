import os
from llama_parse import LlamaParse
import docx
from typing import Dict, Any, Optional, List
import json
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DocumentParser:
    """Document parser that supports PDF, DOC/DOCX, and TXT file formats"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.llmaparse_api_key = api_key or os.getenv("LLMAPARSE_API_KEY")
        if not self.llmaparse_api_key:
            logger.warning("LlamaParse API key not provided")

    def parse_document(self, file_path: str) -> Dict[str, Any]:
        """
        Parse document and return structured data
        
        :param file_path: Path to the document file
        :return: Dictionary containing parsing results
        """
        start_time = datetime.now()
        
        # Get file extension
        file_ext = os.path.splitext(file_path)[1].lower()
        
        try:
            # Choose parsing method based on file type
            if file_ext == '.pdf':
                content = self._parse_pdf(file_path)
            elif file_ext in ['.doc', '.docx']:
                content = self._parse_docx(file_path)
            elif file_ext == '.txt':
                content = self._parse_txt(file_path)
            else:
                raise ValueError(f"Unsupported file format: {file_ext}")

            # Extract document structure and skills
            sections = self._extract_sections(content)
            
            # Calculate processing time
            processing_time = (datetime.now() - start_time).total_seconds()
            
            return {
                "text": content,
                "metadata": {
                    "format": file_ext,
                    "size": os.path.getsize(file_path),
                    "processingTime": processing_time,
                    "sections": sections
                }
            }
            
        except Exception as e:
            logger.error(f"Error parsing document: {str(e)}")
            raise

    def _parse_pdf(self, file_path: str) -> str:
        """Parse PDF file"""
        if not self.llmaparse_api_key:
            raise ValueError("LlamaParse API key is required for PDF parsing")
            
        parser = LlamaParse(api_key=self.llmaparse_api_key, result_type="markdown")
        result = parser.load_data(file_path)
        
        if isinstance(result, list):
            return "\n\n".join(doc.text if hasattr(doc, 'text') else str(doc) for doc in result)
        return result.text if hasattr(result, 'text') else str(result)

    def _parse_docx(self, file_path: str) -> str:
        """Parse DOCX file"""
        doc = docx.Document(file_path)
        return "\n".join([paragraph.text for paragraph in doc.paragraphs])

    def _parse_txt(self, file_path: str) -> str:
        """Parse TXT file"""
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()

    def _extract_sections(self, text: str) -> Dict[str, Any]:
        """Extract different sections from the document"""
        sections = {}
        
        # Extract skills section
        skills_pattern = r'(?:SKILLS?|EXPERTISE|COMPETENCIES?)(?:\r?\n|\:)([^]*?)(?=\r?\n\s*(?:EDUCATION|EXPERIENCE|EMPLOYMENT|$))'
        skills_match = self._find_section(text, skills_pattern)
        if skills_match:
            sections['skills'] = self._parse_skills(skills_match)
            
        # Extract education section
        education_pattern = r'EDUCATION(?:\r?\n|\:)([^]*?)(?=\r?\n\s*(?:EXPERIENCE|EMPLOYMENT|SKILLS?|$))'
        education_match = self._find_section(text, education_pattern)
        if education_match:
            sections['education'] = education_match.strip()
            
        # Extract experience section
        experience_pattern = r'(?:EXPERIENCE|EMPLOYMENT)(?:\r?\n|\:)([^]*?)(?=\r?\n\s*(?:EDUCATION|SKILLS?|$))'
        experience_match = self._find_section(text, experience_pattern)
        if experience_match:
            sections['experience'] = experience_match.strip()
            
        return sections

    def _find_section(self, text: str, pattern: str) -> Optional[str]:
        """Find document section using regex pattern"""
        import re
        match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
        return match.group(1) if match else None

    def _parse_skills(self, skills_text: str) -> List[str]:
        """Parse skills text into a list of skills"""
        # Remove empty lines and extra whitespace
        skills_text = skills_text.strip()
        
        # Split skills (considering commas, semicolons, and line breaks)
        skills = []
        for line in skills_text.split('\n'):
            skills.extend([s.strip() for s in line.split(',') if s.strip()])
            
        # Remove duplicates and sort
        return sorted(list(set(skills)))

# Example usage
if __name__ == "__main__":
    parser = DocumentParser()
    try:
        result = parser.parse_document("example.pdf")
        print(json.dumps(result, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Error: {str(e)}")