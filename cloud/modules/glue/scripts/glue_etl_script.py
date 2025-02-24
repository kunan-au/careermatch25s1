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
import nltk

# --------------------------------------------------
# Step 0: Ensure All NLTK Data is Downloaded
# --------------------------------------------------
def ensure_nltk_resources():
    """
    Forces download of all NLTK data. This is large, but it reliably
    addresses missing resource errors.
    """
    nltk.download('all')  # Comment out if already downloaded

ensure_nltk_resources()

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# --------------------------------------------------
# 1. Data Cleaning Functions
# --------------------------------------------------
def detect_outliers_by_length(df: pd.DataFrame, text_column: str, multiplier: float = 1.5) -> pd.DataFrame:
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
    logging.info("Cleaning dataset: standardizing 'Category' and removing duplicates.")
    if 'Category' in df.columns:
        df['Category'] = df['Category'].astype(str).str.strip().str.upper()
    before = len(df)
    df.drop_duplicates(inplace=True)
    after = len(df)
    logging.info(f"Removed {before - after} duplicate rows; remaining rows: {after}.")
    return df

# --------------------------------------------------
# 2. Data Transformation Functions
# --------------------------------------------------
def extract_plain_text(html_content: Union[str, float]) -> str:
    if pd.isna(html_content) or html_content == "Unknown":
        return "Unknown"
    # Remove HTML tags and unescape entities
    plain_text = re.sub(r'<[^<]+?>', '', html.unescape(str(html_content)))
    return plain_text.strip()

def extract_phone_number(text: str) -> str:
    if text == "Unknown" or pd.isna(text):
        return "Unknown"
    phone_pattern = re.compile(
        r'(\+?\d{1,3}[\s\-()]*)?(?:\(\d{1,4}\)|\d{1,4})[\s\-()]*\d{1,4}[\s\-()]*\d{1,4}(?:\s*x\s*\d+)?'
    )
    match = phone_pattern.search(text)
    return match.group(0).strip() if match else "Unknown"

def extract_email(text: str) -> str:
    if text == "Unknown" or pd.isna(text):
        return "Unknown"
    email_pattern = re.compile(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+')
    match = email_pattern.search(text)
    return match.group(0).strip() if match else "Unknown"

def extract_linkedin_url(text: str) -> str:
    if text == "Unknown" or pd.isna(text):
        return "Unknown"
    pattern = re.compile(r'(https?://(www\.)?linkedin\.com/[^\s]+)')
    match = pattern.search(text)
    return match.group(0).strip() if match else "Unknown"

# Dictionary-based extraction lists
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
    if text == "Unknown" or pd.isna(text):
        return "Unknown"
    found = []
    lower_text = text.lower()
    for kw in keywords_list:
        if kw.lower() in lower_text:
            found.append(kw)
    return "; ".join(sorted(set(found))) if found else "Unknown"

def find_degrees(text: str) -> str:
    return find_keywords(text, DEGREES)

def find_spoken_languages(text: str) -> str:
    return find_keywords(text, LANGUAGES_SPOKEN)

def find_certifications(text: str) -> str:
    if text == "Unknown" or pd.isna(text):
        return "Unknown"
    found = []
    lower_text = text.lower()
    for cert in CERTIFICATIONS:
        if cert.lower() in lower_text:
            found.append(cert)
    return "; ".join(sorted(set(found))) if found else "Unknown"

def spacy_extract_entities(text: str, nlp_obj) -> Dict[str, List[str]]:
    if text == "Unknown" or pd.isna(text):
        return {"PERSON": [], "ORG": [], "GPE": [], "LOC": []}
    doc = nlp_obj(text)
    entities = {"PERSON": set(), "ORG": set(), "GPE": set(), "LOC": set()}
    for ent in doc.ents:
        if ent.label_ in entities:
            entities[ent.label_].add(ent.text.strip())
    return {k: sorted(v) for k, v in entities.items()}

universities_list = [
    "harvard university",
    "stanford university",
    "massachusetts institute of technology",
    "yale university",
    "oxford university",
    "cambridge university"
]

def identify_university(orgs_str: str) -> str:
    if not orgs_str or orgs_str == "Unknown":
        return "Unknown"
    orgs = [o.strip().lower() for o in orgs_str.split(";")]
    for org in orgs:
        for uni in universities_list:
            if uni in org:
                return uni.title()
    return "Unknown"

def extract_years_of_experience(text: str) -> Union[int, str]:
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
        except Exception as e:
            continue
    return max(experiences) if experiences else "Unknown"

def extract_section(text: str, section_name: str) -> str:
    if text == "Unknown" or pd.isna(text):
        return "Unknown"
    pattern = rf'{section_name}[\s\S]*?(?=[A-Z]{{2,}}[\s\n]|$)'
    match = re.search(pattern, text, re.IGNORECASE)
    return match.group(0).strip() if match else "Unknown"

def preprocess_text(text: str) -> str:
    if text == "Unknown" or pd.isna(text):
        return "Unknown"
    text = text.lower()
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    tokens = [t for t in tokens if t.isalpha() and t not in stop_words]
    return " ".join(tokens)

# --------------------------------------------------
# 3. Enhanced ETL Pipeline Processing Function
# --------------------------------------------------
def process_df(df: pd.DataFrame, remove_outliers: bool = False) -> pd.DataFrame:
    """
    Processes the input DataFrame containing resume data:
      - Cleans data (duplicates, outliers)
      - Transforms text (HTML-to-plain text, extractions, NER, etc.)
      - Enriches data with additional metrics and performs basic validations
    """
    # Clean data and remove duplicates
    df = clean_data(df)
    
    # Remove outliers based on resume text length if applicable
    if 'Resume_str' in df.columns:
        outliers = detect_outliers_by_length(df, 'Resume_str')
        if remove_outliers and not outliers.empty:
            df = df[~df.index.isin(outliers.index)]
            logging.info(f"Outliers removed; new shape: {df.shape}")
    
    # Convert HTML to plain text or fallback to the raw string column
    if 'Resume_html' in df.columns:
        df['Resume_text'] = df['Resume_html'].apply(extract_plain_text)
    elif 'Resume_str' in df.columns:
        df.rename(columns={'Resume_str': 'Resume_text'}, inplace=True)
    else:
        logging.warning("No 'Resume_html' or 'Resume_str' found; setting 'Resume_text' to 'Unknown'.")
        df['Resume_text'] = "Unknown"
    
    # Remove extra whitespace in resume text
    df['Resume_text'] = df['Resume_text'].str.strip().replace(r'\s+', ' ', regex=True)
    
    # Basic extractions: Phone, Email, LinkedIn URL
    df['Phone_Number'] = df['Resume_text'].apply(extract_phone_number)
    df['Email_Address'] = df['Resume_text'].apply(extract_email)
    df['LinkedIn_URL'] = df['Resume_text'].apply(extract_linkedin_url)
    
    # Dictionary-based extractions
    df['Soft_Skills'] = df['Resume_text'].apply(lambda x: find_keywords(x, SOFT_SKILLS))
    df['Hard_Skills'] = df['Resume_text'].apply(lambda x: find_keywords(x, SKILL_KEYWORDS))
    df['Programming_Languages'] = df['Resume_text'].apply(lambda x: find_keywords(x, PROGRAMMING_LANGUAGES))
    df['Frameworks'] = df['Resume_text'].apply(lambda x: find_keywords(x, FRAMEWORKS))
    df['Databases'] = df['Resume_text'].apply(lambda x: find_keywords(x, DATABASES))
    df['Cloud_Providers'] = df['Resume_text'].apply(lambda x: find_keywords(x, CLOUD_PROVIDERS))
    df['Degrees'] = df['Resume_text'].apply(find_degrees)
    df['Languages_Spoken'] = df['Resume_text'].apply(find_spoken_languages)
    df['Certifications'] = df['Resume_text'].apply(find_certifications)
    
    # Additional text preprocessing and enrichment
    df['Clean_Tokens'] = df['Resume_text'].apply(preprocess_text)
    df['Word_Count'] = df['Resume_text'].apply(lambda x: len(x.split()) if x != "Unknown" else 0)
    df['Sentence_Count'] = df['Resume_text'].apply(lambda x: len(sent_tokenize(x)) if x != "Unknown" else 0)
    df['Cleaned_Token_Count'] = df['Clean_Tokens'].apply(lambda x: len(x.split()) if x != "Unknown" else 0)
    
    # spaCy Named Entity Recognition
    logging.info("Loading spaCy model for NER...")
    nlp = spacy.load("en_core_web_sm")
    df['spacy_entities'] = df['Resume_text'].apply(lambda x: spacy_extract_entities(x, nlp))
    df['Persons'] = df['spacy_entities'].apply(lambda ents: "; ".join(ents['PERSON']))
    df['Organizations'] = df['spacy_entities'].apply(lambda ents: "; ".join(ents['ORG']))
    df['Locations'] = df['spacy_entities'].apply(lambda ents: "; ".join(sorted(set(ents['GPE'] + ents['LOC']))))
    
    # Identify university, years of experience, and extract sections
    df['University'] = df['Organizations'].apply(identify_university)
    df['Years_of_Experience'] = df['Resume_text'].apply(extract_years_of_experience)
    df['Education_Section'] = df['Resume_text'].apply(lambda x: extract_section(x, "EDUCATION"))
    df['Experience_Section'] = df['Resume_text'].apply(lambda x: extract_section(x, "EXPERIENCE"))
    
    # Normalize word count if an external Word_Count exists (optional)
    if 'Word_Count' in df.columns:
        max_wc = df['Word_Count'].max()
        if pd.notna(max_wc) and max_wc > 0:
            df['Normalized_Word_Count'] = df['Word_Count'] / max_wc
        else:
            df['Normalized_Word_Count'] = "Unknown"
    else:
        df['Normalized_Word_Count'] = "Unknown"
    
    # Basic validation: warn if critical fields remain unknown
    missing_emails = df[df['Email_Address'] == "Unknown"]
    missing_phones = df[df['Phone_Number'] == "Unknown"]
    if not missing_emails.empty:
        logging.warning(f"{len(missing_emails)} rows have unknown email addresses.")
    if not missing_phones.empty:
        logging.warning(f"{len(missing_phones)} rows have unknown phone numbers.")
    
    return df

# --------------------------------------------------
# 4. Main Routine: Read from Database & Write to Glue Catalog/S3
# --------------------------------------------------
if __name__ == "__main__":
    from pyspark.context import SparkContext
    from awsglue.context import GlueContext
    from awsglue.dynamicframe import DynamicFrame

    # ----------------------------
    # Manual Input Variables (update these)
    # ----------------------------
    jdbc_url = "jdbc:mysql://your-db-host:3306/your_db_name"  # Your DB host and name
    user = "your_username"           # Your database username
    password = "your_password"       # Your database password
    table_name = "your_resume_table" # Your table name containing resume data

    glue_database_name = "your_glue_database"  # Your Glue Catalog database name
    glue_table_name = "cleaned_resume"         # Target Glue table name
    output_s3_path = "s3://your-bucket/path/to/output/"  # S3 bucket/path for output

    # ----------------------------
    # Initialize Glue Context and Spark Session
    # ----------------------------
    glueContext = GlueContext(SparkContext.getOrCreate())
    spark = glueContext.spark_session

    # ----------------------------
    # Read from Database (RDS) using JDBC
    # ----------------------------
    logging.info("Reading resume data from the database (RDS)...")
    jdbc_df = spark.read \
        .format("jdbc") \
        .option("url", jdbc_url) \
        .option("dbtable", table_name) \
        .option("user", user) \
        .option("password", password) \
        .load()

    # Convert Spark DataFrame to Pandas DataFrame for ETL processing
    df_pd = jdbc_df.toPandas()

    # ----------------------------
    # Process Data via ETL Pipeline (with enhanced transformations)
    # ----------------------------
    logging.info("Processing resume data through the enhanced ETL pipeline...")
    processed_df = process_df(df_pd, remove_outliers=False)

    # Convert the processed Pandas DataFrame back to a Spark DataFrame
    logging.info("Converting processed data back to Spark DataFrame...")
    processed_spark_df = spark.createDataFrame(processed_df)

    # Convert Spark DataFrame to a Glue DynamicFrame
    logging.info("Converting Spark DataFrame to Glue DynamicFrame...")
    processed_dynamic_frame = DynamicFrame.fromDF(processed_spark_df, glueContext, "processed_dynamic_frame")

    # ----------------------------
    # Write to S3 and Update Glue Data Catalog
    # ----------------------------
    logging.info("Writing processed data to S3 and updating Glue Catalog...")
    datasink = glueContext.getSink(
        connection_type="s3",
        path=output_s3_path,
        enableUpdateCatalog=True,
        partitionKeys=[]
    )
    datasink.setCatalogInfo(
        catalogDatabase=glue_database_name,
        catalogTableName=glue_table_name
    )
    datasink.setFormat("glueparquet")
    datasink.writeFrame(processed_dynamic_frame)

    logging.info("Enhanced ETL pipeline finished successfully.")
