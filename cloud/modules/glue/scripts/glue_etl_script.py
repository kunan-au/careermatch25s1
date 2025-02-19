"""
ETL Pipeline for Resume Data

This script loads a CSV file with resume data, cleans and preprocesses it,
then extracts key information (e.g., phone, email, LinkedIn, universities, certifications)
using regex, dictionaries, and spaCy Named Entity Recognition. Finally, it saves the
enhanced dataset to a new CSV.

Dependencies:
    pip install spacy
    python -m spacy download en_core_web_sm
    pip install word2number  (for converting textual numbers to digits if needed)

Data Assumptions:
    - The CSV contains columns:
        ["Resume_str", "Resume_html", "Category", "Word_Count", ...]
    - We'll save the transformed dataset as "Cleaned_Resume.csv" at the same or a specified path.
"""

import pandas as pd
import numpy as np
import re
import html
import spacy
from spacy.matcher import Matcher
from word2number import w2n  # for converting textual numbers to digits

##############################
# Step 1: Load the Dataset
##############################
file_path = "/content/Resume.csv"  # <-- Update this if needed
try:
    df = pd.read_csv(file_path, encoding='utf-8')
except UnicodeDecodeError:
    df = pd.read_csv(file_path, encoding='ISO-8859-1')

# Fill all missing values with "Unknown"
df.fillna("Unknown", inplace=True)

##############################
# Step 2: Data Cleaning
##############################

# 2.1 Detecting and Handling Outliers (based on text length)
def detect_outliers_by_length(df, column):
    lengths = df[column].apply(lambda x: len(str(x)))
    q1, q3 = np.percentile(lengths, [25, 75])
    iqr = q3 - q1
    lower_bound, upper_bound = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    return df[(lengths < lower_bound) | (lengths > upper_bound)]

outliers = detect_outliers_by_length(df, "Resume_str")
print(f"Number of detected outliers by length: {len(outliers)}")

# (Optional) Remove outliers:
# df = df[~df.index.isin(outliers.index)]

# 2.2 Fix Inconsistencies & Duplicate Entries
# Standardize Category to uppercase
df['Category'] = df['Category'].str.strip().str.upper()

# Drop duplicates
df.drop_duplicates(inplace=True)

##############################
# Step 3: Data Transformation
##############################

# 3.1 Convert HTML to Plain Text
def extract_plain_text(html_content):
    if pd.isna(html_content):
        return "Unknown"
    # Remove HTML tags and decode HTML entities
    plain_text = re.sub(r'<[^<]+?>', '', html.unescape(str(html_content)))
    return plain_text.strip()

df['Resume_text'] = df['Resume_html'].apply(extract_plain_text)

# 3.2 Basic Regex/Dictionaries for Key Fields

# Extract Skills (as an example of looking for a "Skills" section)
def extract_skills(text):
    if pd.isna(text) or text == "Unknown":
        return "Unknown"
    # Regex tries to capture everything after "Skills" until the next capitalized heading or end
    match = re.search(r"(Skills|SKILLS)[\s\S]*?(?=[A-Z][a-z]|$)", text)
    return match.group(0).strip() if match else "Unknown"

df['Extracted_Skills'] = df['Resume_text'].apply(extract_skills)

# Extract Phone Number
def extract_phone_number(text):
    if pd.isna(text) or text == "Unknown":
        return "Unknown"
    # Example pattern for phone: +1 (123) 456-7890, 123-456-7890, etc.
    phone_pattern = re.compile(r'(\+?\d[\d\-\(\)\s]{7,}\d)')
    match = phone_pattern.search(text)
    return match.group(0).strip() if match else "Unknown"

df['Phone_Number'] = df['Resume_text'].apply(extract_phone_number)

# Extract Email
def extract_email(text):
    if pd.isna(text) or text == "Unknown":
        return "Unknown"
    email_pattern = re.compile(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+')
    match = email_pattern.search(text)
    return match.group(0).strip() if match else "Unknown"

df['Email_Address'] = df['Resume_text'].apply(extract_email)

# Extract LinkedIn URL
def extract_linkedin_url(text):
    if pd.isna(text) or text == "Unknown":
        return "Unknown"
    linkedin_pattern = re.compile(r'(https?://(www\.)?linkedin\.com/[^\s]+)')
    match = linkedin_pattern.search(text)
    return match.group(0).strip() if match else "Unknown"

df['LinkedIn_URL'] = df['Resume_text'].apply(extract_linkedin_url)

# Extract Certifications (Dictionary-based)
CERTIFICATIONS = [
    "PMP", "CFA", "AWS Certified Solutions Architect",
    "Certified Scrum Master", "CISSP"
]

def find_certifications(text):
    if pd.isna(text) or text == "Unknown":
        return "Unknown"
    found = []
    for cert in CERTIFICATIONS:
        # Use a case-insensitive search
        pattern = re.compile(re.escape(cert), re.IGNORECASE)
        if pattern.search(text):
            found.append(cert)
    return "; ".join(found) if found else "Unknown"

df['Certifications'] = df['Resume_text'].apply(find_certifications)

# 3.3 Named Entity Recognition with spaCy
nlp = spacy.load("en_core_web_sm")  # Ensure you've run "python -m spacy download en_core_web_sm" beforehand

def spacy_extract_entities(text):
    if pd.isna(text) or text == "Unknown":
        return {"PERSON": [], "ORG": [], "GPE": [], "LOC": []}

    doc = nlp(text)
    entities = {"PERSON": set(), "ORG": set(), "GPE": set(), "LOC": set()}
    
    for ent in doc.ents:
        if ent.label_ in entities:
            entities[ent.label_].add(ent.text.strip())
    
    # Convert sets to lists
    return {k: list(v) for k, v in entities.items()}

df['spacy_entities'] = df['Resume_text'].apply(spacy_extract_entities)

# For convenience, flatten them into separate columns:
df['Persons'] = df['spacy_entities'].apply(lambda x: "; ".join(x["PERSON"]))
df['Organizations'] = df['spacy_entities'].apply(lambda x: "; ".join(x["ORG"]))
df['Locations'] = df['spacy_entities'].apply(lambda x: "; ".join(x["GPE"] + x["LOC"]))

# Identify University from recognized ORG entities
universities_list = [
    "Harvard University", "Stanford University", "Massachusetts Institute of Technology",
    "Yale University", "Oxford University", "Cambridge University"
    # Add more as needed...
]

def identify_university(orgs_str):
    # 'orgs_str' is something like "Google; Stanford University; ABC Inc"
    if orgs_str == "":
        return "Unknown"
    
    orgs = [o.strip() for o in orgs_str.split(";")]
    for org in orgs:
        for uni in universities_list:
            if uni.lower() in org.lower():
                return uni
    return "Unknown"

df['University'] = df['Organizations'].apply(identify_university)

##########################
# 3.4 Additional Extractions
##########################

# Extract "Years of Experience" using text patterns + word2number
def extract_years_of_experience(text):
    """
    1) Look for patterns like 'X years of experience'.
    2) Convert spelled-out numbers to digits using word2number if found.
    3) Return the maximum found if multiple references exist.
    """
    if pd.isna(text) or text == "Unknown":
        return "Unknown"
    
    pattern = re.compile(r'(\d+|one|two|three|four|five|six|seven|eight|nine|ten)\s+years?\s+of\s+experience', re.IGNORECASE)
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
    
    if experiences:
        return max(experiences)  # or sum(experiences), depending on your preference
    return "Unknown"

df['Years_of_Experience'] = df['Resume_text'].apply(extract_years_of_experience)

##########################
# 3.5 Word Count Normalization
##########################
# Check if 'Word_Count' exists; otherwise skip
if 'Word_Count' in df.columns:
    max_word_count = df['Word_Count'].max()
    if pd.notna(max_word_count) and max_word_count != 0:
        df['Normalized_Word_Count'] = df['Word_Count'] / max_word_count
    else:
        df['Normalized_Word_Count'] = "Unknown"
else:
    df['Normalized_Word_Count'] = "Unknown"

##########################
# Step 4: Save the Transformed Data
##########################
output_path = "/content/Cleaned_Resume.csv"
df.to_csv(output_path, index=False, encoding='utf-8')
print(f"Cleaned dataset saved at: {output_path}")
