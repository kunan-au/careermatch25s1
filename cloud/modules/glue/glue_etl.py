import sys
import logging
import re
import pandas as pd
from bs4 import BeautifulSoup
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.sql import SparkSession
from awsglue.context import GlueContext
from awsglue.job import Job

# Setup logging
logging.basicConfig(filename="etl_logs.log", level=logging.INFO, format="%(asctime)s - %(message)s")

# Parse AWS Glue arguments
args = getResolvedOptions(sys.argv, [
    "JOB_NAME",
    "s3_raw_data_path",
    "s3_curated_path"
])

# Initialize Spark and Glue Context
spark = SparkSession.builder.appName("ETLJob").getOrCreate()
glueContext = GlueContext(spark.sparkContext)
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

# Define S3 paths
raw_data_path = "s3://" + args["s3_raw_data_path"] + "/raw-data/"
curated_data_path = "s3://" + args["s3_curated_path"] + "/cleaned-data/"

logging.info("Loading raw resume data from: " + raw_data_path)

# Load raw data from S3
df = spark.read.option("header", True).csv(raw_data_path)

# Function to clean HTML content
def clean_html(text):
    if text is None or not isinstance(text, str):
        return ""
    text = BeautifulSoup(text, "html.parser").get_text()
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# Function to clean text
def clean_text(text):
    if text is None or not isinstance(text, str):
        return ""
    text = re.sub(r'[^\x00-\x7F]+', '', text)  # Remove non-ASCII
    text = re.sub(r'\s+', ' ', text)  # Normalize spaces
    text = re.sub(r'[^\w\s.,!?-]', '', text)  # Remove special characters
    return text.lower().strip()

# Function to extract emails
def extract_email(text):
    match = re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', text)
    return match[0] if match else None

# Function to extract phone numbers
def extract_phone(text):
    match = re.findall(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', text)
    return match[0] if match else None

# Function to extract skills dynamically based on the Category column
def extract_skills(text, category):
    if category is None or text is None:
        return ""
    category_words = category.split()
    found_skills = [word for word in category_words if word.lower() in text.lower()]
    return ", ".join(found_skills) if found_skills else None

# Apply transformations
df = df.withColumn("Resume_clean", df["Resume_html"].cast("string"))
df = df.withColumn("Resume_clean", df["Resume_clean"].apply(clean_html))
df = df.withColumn("Resume_clean", df["Resume_clean"].apply(clean_text))
df = df.withColumn("Resume_summary", df["Resume_s"].apply(clean_text))
df = df.withColumn("Email", df["Resume_clean"].apply(extract_email))
df = df.withColumn("Phone", df["Resume_clean"].apply(extract_phone))
df = df.withColumn("Extracted_Skills", df.apply(lambda row: extract_skills(row["Resume_clean"], row["Category"]), axis=1))

# Drop unwanted columns
df = df.drop("Resume_html", "Resume_s")

# Remove duplicates
df = df.dropDuplicates(["ID"])

# Save cleaned data to the curated S3 bucket
df.write.mode("overwrite").parquet(curated_data_path)

logging.info("✅ Cleaned Data Saved to: " + curated_data_path)

# Commit job
job.commit()
