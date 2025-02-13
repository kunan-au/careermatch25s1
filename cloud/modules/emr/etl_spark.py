from pyspark.sql import SparkSession
from pyspark.sql.functions import col

# Initialize Spark session
spark = SparkSession.builder.appName("EcommerceETL").getOrCreate()

# Define S3 paths
input_path = "s3://ecommerce-raw-data/orders/"
output_path = "s3://ecommerce-curated-data/orders_processed/"

# Load raw data from S3
df = spark.read.option("header", True).csv(input_path)

# Perform data transformations
df_cleaned = df.select(
    col("order_id").cast("integer"),
    col("customer_id").cast("integer"),
    col("order_date").cast("date"),
    col("total_amount").cast("float")
).dropna()

# Write processed data back to S3
df_cleaned.write.mode("overwrite").parquet(output_path)

print("ETL Job Completed Successfully")

# Stop Spark session
spark.stop()

# Upload Spark Job to S3
# aws s3 cp modules/emr/etl_spark.py s3://my-emr-scripts/
