import re
import html
import logging
from typing import Union, List
from dateutil import parser as date_parser

import pandas as pd
import numpy as np
import spacy
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

def ensure_nltk_resources():
    nltk.download('punkt')
    nltk.download('stopwords')

ensure_nltk_resources()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# --------------------------------------------------
# 1. Data Cleaning and Preprocessing Functions
# --------------------------------------------------
def extract_plain_text(html_content: Union[str, float]) -> str:
    """
    Converts HTML content to plain text.
    """
    if pd.isna(html_content) or html_content == "Unknown":
        return "Unknown"
    plain_text = re.sub(r'<[^<]+?>', '', html.unescape(str(html_content)))
    return plain_text.strip()

def preprocess_text(text: str) -> str:
    """
    Lowercases text, tokenizes, removes non-alphabetic tokens and stop words.
    """
    if pd.isna(text) or text == "Unknown":
        return "Unknown"
    text = text.lower()
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    tokens = [t for t in tokens if t.isalpha() and t not in stop_words]
    return " ".join(tokens)

def extract_salary(salary_text: Union[str, float]) -> str:
    """
    Extracts the first numeric salary value found in the salary string.
    """
    if pd.isna(salary_text) or str(salary_text).strip() == "":
        return "Unknown"
    salary_text = str(salary_text).replace("Â", "").replace(",", "")
    match = re.search(r'([\d\.]+)', salary_text)
    return match.group(1) if match else "Unknown"

def parse_listing_date(date_str: Union[str, float]) -> str:
    """
    Parses the listing date and converts it to YYYY-MM-DD format.
    """
    if pd.isna(date_str) or str(date_str).strip() == "":
        return "Unknown"
    try:
        dt = date_parser.parse(str(date_str))
        return dt.strftime("%Y-%m-%d")
    except Exception:
        return "Unknown"

def find_keywords_job(text: str, keywords_list: List[str]) -> str:
    """
    Searches for job-specific keywords within the text.
    """
    if pd.isna(text) or text == "Unknown":
        return "Unknown"
    found = []
    lower_text = text.lower()
    for kw in keywords_list:
        if kw.lower() in lower_text:
            found.append(kw)
    return "; ".join(sorted(set(found))) if found else "Unknown"

# Define a list of job-related keywords (adjust as needed)
JOB_SKILL_KEYWORDS = [
    "procurement", "accounting", "data analysis", "engineering", "sales",
    "administration", "hr", "marketing", "software", "quality assurance",
    "customer service", "project management"
]

def extract_experience(text: str) -> Union[int, str]:
    """
    Extracts the maximum number of years of experience mentioned in the text.
    """
    if pd.isna(text) or text == "Unknown":
        return "Unknown"
    pattern = re.compile(
        r'(\d+)\s*(?:\+|plus)?\s*(?:years|yrs)\s+of\s+experience',
        re.IGNORECASE
    )
    matches = pattern.findall(text)
    if matches:
        try:
            experiences = [int(m) for m in matches]
            return max(experiences)
        except:
            return "Unknown"
    else:
        return "Unknown"

def extract_section(text: str, section_name: str) -> str:
    """
    Extracts a section of the text that starts with the given section name.
    """
    if pd.isna(text) or text == "Unknown":
        return "Unknown"
    pattern = rf'{section_name}[\s\S]*?(?=\n[A-Z][a-z]+:|$)'
    match = re.search(pattern, text, re.IGNORECASE)
    return match.group(0).strip() if match else "Unknown"

# --------------------------------------------------
# 2. spaCy Named Entity Extraction Function
# --------------------------------------------------
def spacy_extract_entities(text: str, nlp_obj) -> dict:
    """
    Uses spaCy to extract entities (PERSON, ORG, GPE) from text.
    """
    if pd.isna(text) or text == "Unknown":
        return {"PERSON": [], "ORG": [], "GPE": []}
    doc = nlp_obj(text)
    entities = {"PERSON": set(), "ORG": set(), "GPE": set()}
    for ent in doc.ents:
        if ent.label_ in entities:
            entities[ent.label_].add(ent.text.strip())
    return {k: sorted(v) for k, v in entities.items()}

# --------------------------------------------------
# 3. ETL Pipeline Processing Function for Job Descriptions
# --------------------------------------------------
def process_job_descriptions(df: pd.DataFrame) -> pd.DataFrame:
    logging.info("Starting processing of job description data...")

    # Remove duplicate rows
    before = len(df)
    df.drop_duplicates(inplace=True)
    after = len(df)
    logging.info(f"Removed {before - after} duplicate rows; remaining rows: {after}.")

    # Clean and preprocess the 'descriptions' field
    df['Description_Text'] = df['descriptions'].apply(
        lambda x: extract_plain_text(x) if isinstance(x, str) else "Unknown"
    )
    df['Description_Text'] = df['Description_Text'].str.strip().replace(r'\s+', ' ', regex=True)

    # Preprocess the text for analysis
    df['Cleaned_Description'] = df['Description_Text'].apply(preprocess_text)

    # Calculate word and sentence counts
    df['Word_Count'] = df['Description_Text'].apply(lambda x: len(x.split()) if x != "Unknown" else 0)
    df['Sentence_Count'] = df['Description_Text'].apply(lambda x: len(sent_tokenize(x)) if x != "Unknown" else 0)
    max_wc = df['Word_Count'].max() if df['Word_Count'].max() > 0 else 1
    df['Normalized_Word_Count'] = df['Word_Count'] / max_wc

    # Extract salary information
    df['Extracted_Salary'] = df['salary'].apply(
        lambda x: extract_salary(x) if isinstance(x, str) else "Unknown"
    )

    # Parse and standardize the listing date
    df['Parsed_ListingDate'] = df['listingDate'].apply(
        lambda x: parse_listing_date(x) if isinstance(x, str) else "Unknown"
    )

    # Extract job skills keywords from the description
    df['Job_Skills'] = df['Description_Text'].apply(lambda x: find_keywords_job(x, JOB_SKILL_KEYWORDS))

    # Extract years of experience mentioned in the description
    df['Required_Experience'] = df['Description_Text'].apply(extract_experience)

    # Extract specific sections (if available)
    df['Responsibilities_Section'] = df['Description_Text'].apply(lambda x: extract_section(x, "Responsibilities"))
    df['Requirements_Section'] = df['Description_Text'].apply(lambda x: extract_section(x, "Requirements"))

    # Apply spaCy NER to extract entities
    logging.info("Loading spaCy model for NER on job descriptions...")
    nlp = spacy.load("en_core_web_sm")
    df['spacy_entities'] = df['Description_Text'].apply(lambda x: spacy_extract_entities(x, nlp))
    df['Extracted_Locations'] = df['spacy_entities'].apply(lambda ents: "; ".join(ents.get('GPE', [])))

    logging.info("Job description ETL processing completed.")
    return df

# --------------------------------------------------
# 4. Main Routine: Read CSV & Write Processed Data
# --------------------------------------------------
if __name__ == "__main__":
    # Update the path as needed
    input_csv = "/content/job_listings.csv"
    logging.info(f"Reading job listings from {input_csv}...")
    df_jobs = pd.read_csv(input_csv)

    logging.info("Processing job descriptions...")
    processed_df = process_job_descriptions(df_jobs)

    # Save the processed DataFrame to a new CSV file
    output_csv = "Processed_JobListing.csv"
    processed_df.to_csv(output_csv, index=False)
    logging.info(f"Processed job description data saved to {output_csv}")