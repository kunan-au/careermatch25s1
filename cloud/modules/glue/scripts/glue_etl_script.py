"""
Enhanced ETL Pipeline for Resume Data
=====================================

Summary:
--------
1. Forces a download of *all* NLTK data to avoid 'punkt_tab' lookup errors.
2. Loads a CSV of resumes (with 'Resume_str' or 'Resume_html') into a DataFrame.
3. Cleans the data (handling outliers, duplicates, missing fields).
4. Transforms the data:
   - Extract phone numbers, emails, LinkedIn URLs
   - Extract dictionaries of skills, degrees, languages, certifications, etc.
   - spaCy NER for persons, organizations, locations
   - Regex-based extraction of Education/Experience sections
   - Basic text preprocessing and word count normalization
5. Saves the enriched DataFrame to a CSV.

Requirements:
-------------
- pip install pandas numpy spacy word2number nltk
- python -m spacy download en_core_web_sm

Usage:
------
python etl_resume_pipeline.py
"""

import re
import html
import logging
from typing import Union, List, Dict

import pandas as pd
import numpy as np
import spacy
from word2number import w2n

# --------------------------------------------------
# Step 0: Ensure All NLTK Data is Downloaded
# --------------------------------------------------
import nltk

def ensure_nltk_resources():
    """
    Forces download of all NLTK data. This is large, but it reliably
    addresses the 'punkt_tab' missing error in some environments.
    """
    nltk.download('all')  # Comment this out if your environment already has the data

ensure_nltk_resources()

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# --------------------------------------------------
# 1. Load Data
# --------------------------------------------------
def load_resume_data(file_path: str) -> pd.DataFrame:
    """
    Loads the CSV file containing resume data.
    - Tries utf-8 and falls back to ISO-8859-1 if needed.
    - Fills missing values with 'Unknown'.
    """
    logging.info(f"Loading data from {file_path}")
    try:
        df = pd.read_csv(file_path, encoding='utf-8')
    except UnicodeDecodeError:
        logging.warning("UTF-8 decoding failed. Trying ISO-8859-1 encoding.")
        df = pd.read_csv(file_path, encoding='ISO-8859-1')

    df.fillna("Unknown", inplace=True)
    logging.info(f"Loaded dataset with {len(df)} rows and {len(df.columns)} columns.")
    return df

# --------------------------------------------------
# 2. Data Cleaning
# --------------------------------------------------
def detect_outliers_by_length(df: pd.DataFrame, text_column: str, multiplier: float = 1.5) -> pd.DataFrame:
    """
    Detect outliers based on the IQR (interquartile range) of text length
    in 'text_column'. Returns a DataFrame containing only the outlier rows.
    """
    logging.info(f"Detecting outliers by text length in '{text_column}'...")
    lengths = df[text_column].apply(lambda x: len(str(x)))
    q1, q3 = np.percentile(lengths, [25, 75])
    iqr = q3 - q1
    lower_bound = q1 - multiplier * iqr
    upper_bound = q3 + multiplier * iqr
    outliers = df[(lengths < lower_bound) | (lengths > upper_bound)]
    logging.info(f"Number of detected outliers: {len(outliers)}")
    return outliers

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standard data cleaning steps:
    - Convert 'Category' to uppercase (if it exists).
    - Drop duplicates.
    """
    logging.info("Cleaning dataset (standardizing 'Category', removing duplicates).")
    if 'Category' in df.columns:
        df['Category'] = df['Category'].astype(str).str.strip().str.upper()

    before = len(df)
    df.drop_duplicates(inplace=True)
    after = len(df)
    logging.info(f"Removed {before - after} duplicates; new row count is {len(df)}.")
    return df

# --------------------------------------------------
# 3. Data Transformation
# --------------------------------------------------

# 3.1 Convert HTML to Plain Text
def extract_plain_text(html_content: Union[str, float]) -> str:
    """
    Strips HTML tags and decodes entities. If content is invalid, returns 'Unknown'.
    """
    if pd.isna(html_content) or html_content == "Unknown":
        return "Unknown"
    plain_text = re.sub(r'<[^<]+?>', '', html.unescape(str(html_content)))
    return plain_text.strip()

# 3.2 Extract Basic Fields: Phone, Email, LinkedIn
def extract_phone_number(text: str) -> str:
    """
    Captures phone patterns including optional country code (+xx) and extension (x123).
    """
    if text == "Unknown" or pd.isna(text):
        return "Unknown"
    phone_pattern = re.compile(
        r'(\+?\d{1,3}[\s\-()]*)?(?:\(\d{1,4}\)|\d{1,4})[\s\-()]*\d{1,4}[\s\-()]*\d{1,4}(?:\s*x\s*\d+)?'
    )
    match = phone_pattern.search(text)
    return match.group(0).strip() if match else "Unknown"

def extract_email(text: str) -> str:
    """
    Finds an email address using a straightforward regex.
    """
    if text == "Unknown" or pd.isna(text):
        return "Unknown"
    email_pattern = re.compile(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+')
    match = email_pattern.search(text)
    return match.group(0).strip() if match else "Unknown"

def extract_linkedin_url(text: str) -> str:
    """
    Searches for a LinkedIn URL in the text.
    """
    if text == "Unknown" or pd.isna(text):
        return "Unknown"
    pattern = re.compile(r'(https?://(www\.)?linkedin\.com/[^\s]+)')
    match = pattern.search(text)
    return match.group(0).strip() if match else "Unknown"

# 3.3 Dictionary-Based Extractions: Skills, Degrees, Languages, etc.
SKILL_KEYWORDS = [
    "python", "sql", "excel", "machine learning", "nlp",
    "aws", "azure", "java", "c++", "tableau", "power bi"
]

SOFT_SKILLS = [
    "communication", "teamwork", "leadership", "problem solving",
    "time management", "adaptability", "creativity"
]

PROGRAMMING_LANGUAGES = [
    "python", "java", "c++", "c#", "javascript", "ruby", "go", "php"
]

FRAMEWORKS = [
    "django", "flask", "spring", "react", "angular", "vue", "node.js"
]

DATABASES = [
    "mysql", "postgresql", "mongodb", "oracle", "sql server", "sqlite"
]

CLOUD_PROVIDERS = [
    "aws", "azure", "google cloud", "gcp", "ibm cloud"
]

LANGUAGES_SPOKEN = [
    "english", "spanish", "french", "german", "mandarin", "hindi", "arabic", "portuguese"
]

DEGREES = [
    "bachelor", "master", "phd", "mba", "b.sc", "m.sc",
    "btech", "mtech", "ba", "ma"
]

CERTIFICATIONS = [
    "pmp",
    "cfa",
    "aws certified solutions architect",
    "certified scrum master",
    "cissp"
]

def find_keywords(text: str, keywords_list: List[str]) -> str:
    """
    Helper function for case-insensitive substring searches. Returns
    a '; ' joined list of matches or 'Unknown' if none found.
    """
    if text == "Unknown" or pd.isna(text):
        return "Unknown"
    found = []
    lower_text = text.lower()
    for kw in keywords_list:
        if kw.lower() in lower_text:
            found.append(kw)
    return "; ".join(sorted(set(found))) if found else "Unknown"

def find_degrees(text: str) -> str:
    """
    Looks for references to known degrees (Bachelor, Master, PhD, etc.).
    """
    return find_keywords(text, DEGREES)

def find_spoken_languages(text: str) -> str:
    """
    Detect references to known spoken languages.
    """
    return find_keywords(text, LANGUAGES_SPOKEN)

def find_certifications(text: str) -> str:
    """
    Detect references to known certifications in the text.
    """
    if text == "Unknown" or pd.isna(text):
        return "Unknown"
    found = []
    lower_text = text.lower()
    for cert in CERTIFICATIONS:
        if cert.lower() in lower_text:
            found.append(cert)
    return "; ".join(sorted(set(found))) if found else "Unknown"

# 3.4 Named Entity Recognition (spaCy)
def spacy_extract_entities(text: str, nlp_obj) -> Dict[str, List[str]]:
    """
    Extracts PERSON, ORG, GPE, LOC using spaCy, returning a dictionary of sets.
    """
    if text == "Unknown" or pd.isna(text):
        return {"PERSON": [], "ORG": [], "GPE": [], "LOC": []}

    doc = nlp_obj(text)
    entities = {"PERSON": set(), "ORG": set(), "GPE": set(), "LOC": set()}
    for ent in doc.ents:
        if ent.label_ in entities:
            entities[ent.label_].add(ent.text.strip())
    return {k: sorted(v) for k, v in entities.items()}

# 3.5 Identify University
universities_list = [
    "harvard university",
    "stanford university",
    "massachusetts institute of technology",
    "yale university",
    "oxford university",
    "cambridge university"
]

def identify_university(orgs_str: str) -> str:
    """
    If any recognized ORG entity matches a known university, return it.
    Otherwise return 'Unknown'.
    """
    if not orgs_str or orgs_str == "Unknown":
        return "Unknown"
    orgs = [o.strip().lower() for o in orgs_str.split(";")]
    for org in orgs:
        for uni in universities_list:
            if uni in org:
                return uni.title()  # e.g., "Harvard University"
    return "Unknown"

# 3.6 Extract Years of Experience
def extract_years_of_experience(text: str) -> Union[int, str]:
    """
    Uses a regex to find references like 'X years of experience'.
    Converts textual numbers (one, two, etc.) to digits. Returns the max found.
    """
    if text == "Unknown" or pd.isna(text):
        return "Unknown"

    pattern = re.compile(
        r'(\d+|one|two|three|four|five|six|seven|eight|nine|ten)\s+years?\s+of\s+experience',
        re.IGNORECASE
    )
    matches = pattern.findall(text)
    if not matches:
        return "Unknown"

    experiences = []
    for match in matches:
        try:
            if match.isdigit():
                experiences.append(int(match))
            else:
                experiences.append(w2n.word_to_num(match))
        except:
            continue
    return max(experiences) if experiences else "Unknown"

# 3.7 Extract Education/Experience Sections
def extract_section(text: str, section_name: str) -> str:
    """
    Attempts to capture an entire section from a heading like 'EDUCATION'
    up to the next all-caps heading or the end of the document.
    """
    if text == "Unknown" or pd.isna(text):
        return "Unknown"

    pattern = rf'{section_name}[\s\S]*?(?=[A-Z]{{2,}}[\s\n]|$)'
    match = re.search(pattern, text, re.IGNORECASE)
    return match.group(0).strip() if match else "Unknown"

# 3.8 Text Preprocessing
def preprocess_text(text: str) -> str:
    """
    - Lowercases
    - Tokenizes
    - Removes non-alpha tokens and English stopwords
    - Returns a space-joined string
    """
    if text == "Unknown" or pd.isna(text):
        return "Unknown"

    text = text.lower()
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    tokens = [t for t in tokens if t.isalpha() and t not in stop_words]
    return " ".join(tokens)

# --------------------------------------------------
# 4. ETL Pipeline
# --------------------------------------------------
def etl_pipeline(
    file_path: str,
    output_path: str = "Cleaned_Resume.csv",
    remove_outliers: bool = False
) -> None:
    """
    Orchestrates the end-to-end ETL process:
      1) Load data
      2) Clean (duplicates, outliers)
      3) Transform (HTML -> text, extract phone/email/etc.)
      4) spaCy NER
      5) Save the final dataset
    """
    logging.info("----- Starting ETL Pipeline -----")

    # 1. Load
    df = load_resume_data(file_path)

    # 2. Clean
    df = clean_data(df)

    # 2.1 Detect (optionally remove) outliers by length
    if 'Resume_str' in df.columns:
        outliers = detect_outliers_by_length(df, 'Resume_str')
        if remove_outliers and not outliers.empty:
            df = df[~df.index.isin(outliers.index)]
            logging.info(f"Outliers removed. New shape: {df.shape}")

    # 3. Transform
    # 3.1 Convert HTML -> plain text
    if 'Resume_html' in df.columns:
        df['Resume_text'] = df['Resume_html'].apply(extract_plain_text)
    else:
        # fallback if only 'Resume_str' is present
        if 'Resume_str' in df.columns:
            df.rename(columns={'Resume_str': 'Resume_text'}, inplace=True)
        else:
            logging.warning("No 'Resume_html' or 'Resume_str' found; defaulting 'Resume_text' to 'Unknown'.")
            df['Resume_text'] = "Unknown"

    # 3.2 Basic extractions
    df['Phone_Number'] = df['Resume_text'].apply(extract_phone_number)
    df['Email_Address'] = df['Resume_text'].apply(extract_email)
    df['LinkedIn_URL'] = df['Resume_text'].apply(extract_linkedin_url)

    # 3.3 Additional dictionary-based columns
    df['Soft_Skills'] = df['Resume_text'].apply(lambda x: find_keywords(x, SOFT_SKILLS))
    df['Hard_Skills'] = df['Resume_text'].apply(lambda x: find_keywords(x, SKILL_KEYWORDS))
    df['Programming_Languages'] = df['Resume_text'].apply(lambda x: find_keywords(x, PROGRAMMING_LANGUAGES))
    df['Frameworks'] = df['Resume_text'].apply(lambda x: find_keywords(x, FRAMEWORKS))
    df['Databases'] = df['Resume_text'].apply(lambda x: find_keywords(x, DATABASES))
    df['Cloud_Providers'] = df['Resume_text'].apply(lambda x: find_keywords(x, CLOUD_PROVIDERS))
    df['Degrees'] = df['Resume_text'].apply(find_degrees)
    df['Languages_Spoken'] = df['Resume_text'].apply(find_spoken_languages)
    df['Certifications'] = df['Resume_text'].apply(find_certifications)

    # 3.4 Preprocess text
    df['Clean_Tokens'] = df['Resume_text'].apply(preprocess_text)

    # 3.5 spaCy NER
    logging.info("Loading spaCy model for NER...")
    nlp = spacy.load("en_core_web_sm")
    df['spacy_entities'] = df['Resume_text'].apply(lambda x: spacy_extract_entities(x, nlp))
    df['Persons'] = df['spacy_entities'].apply(lambda ents: "; ".join(ents['PERSON']))
    df['Organizations'] = df['spacy_entities'].apply(lambda ents: "; ".join(ents['ORG']))
    df['Locations'] = df['spacy_entities'].apply(
        lambda ents: "; ".join(sorted(set(ents['GPE'] + ents['LOC'])))
    )

    # 3.6 Identify University
    df['University'] = df['Organizations'].apply(identify_university)

    # 3.7 Extract years of experience
    df['Years_of_Experience'] = df['Resume_text'].apply(extract_years_of_experience)

    # 3.8 Extract Education/Experience sections
    df['Education_Section'] = df['Resume_text'].apply(lambda x: extract_section(x, "EDUCATION"))
    df['Experience_Section'] = df['Resume_text'].apply(lambda x: extract_section(x, "EXPERIENCE"))

    # 3.9 Word Count Normalization
    if 'Word_Count' in df.columns:
        max_wc = df['Word_Count'].max()
        if pd.notna(max_wc) and max_wc > 0:
            df['Normalized_Word_Count'] = df['Word_Count'] / max_wc
        else:
            df['Normalized_Word_Count'] = "Unknown"
    else:
        df['Normalized_Word_Count'] = "Unknown"

    # 4. Save final
    df.to_csv(output_path, index=False, encoding='utf-8')
    logging.info(f"ETL complete. Final dataset saved to {output_path} with {len(df)} rows.")

    logging.info("----- ETL Pipeline Finished Successfully -----")


# --------------------------------------------------
# Script Entry Point
# --------------------------------------------------
if __name__ == "__main__":
    input_csv_path = "/content/Resume.csv"         # Change as needed
    output_csv_path = "/content/Cleaned_Resume.csv"  # Change as needed
    etl_pipeline(file_path=input_csv_path, output_path=output_csv_path, remove_outliers=False)