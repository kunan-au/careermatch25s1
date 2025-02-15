import sys
import boto3
import pyspark.sql.functions as F
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.context import SparkContext
from pyspark.sql import SparkSession
from awsglue.utils import getResolvedOptions
import pymysql

# Get input arguments from Terraform
args = getResolvedOptions(sys.argv, ["S3_INPUT_PATH", "RDS_ENDPOINT", "RDS_USER", "RDS_PASSWORD", "RDS_DATABASE"])

# Initialize Glue and Spark
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

# Read raw data from S3
df = spark.read.option("header", "true").csv(args["S3_INPUT_PATH"])

# Data Transformation: Convert age to integer
df = df.withColumn("age", F.col("age").cast("int"))

# Convert DataFrame to Pandas
pandas_df = df.toPandas()

# Connect to RDS
conn = pymysql.connect(
    host=args["RDS_ENDPOINT"],
    user=args["RDS_USER"],
    password=args["RDS_PASSWORD"],
    database=args["RDS_DATABASE"]
)
cursor = conn.cursor()

# Create Table (if not exists)
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT PRIMARY KEY,
        name VARCHAR(255),
        email VARCHAR(255),
        age INT,
        city VARCHAR(255)
    )
""")

# Insert Data into RDS
for _, row in pandas_df.iterrows():
    cursor.execute("INSERT INTO users (id, name, email, age, city) VALUES (%s, %s, %s, %s, %s)", 
                   (row["id"], row["name"], row["email"], row["age"], row["city"]))

conn.commit()
cursor.close()
conn.close()

print("✅ Glue ETL Completed: Data Loaded into RDS!")
