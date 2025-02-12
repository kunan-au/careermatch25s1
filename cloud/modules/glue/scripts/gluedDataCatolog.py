import sys
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.dynamicframe import DynamicFrame

# Initialize Glue Context
glueContext = GlueContext(SparkContext.getOrCreate())
spark = glueContext.spark_session

# RDS Database Configuration
database_name = "imba"
jdbc_url = ""
user = ""
password = ""

# Your Glue Data Catalog database name
glue_database_name = ""

# S3 bucket path where data will be written
output_s3_path = ""

# List of tables to copy from RDS to Glue Data Catalog
table_list = [
    "aisles", 
    "departments", 
    "order_products_prior", 
    "order_products_train", 
    "orders", 
    "products"
]

for table_name in table_list:
    print(f"Reading data from RDS table: {table_name}")

    # Read the table from RDS
    jdbc_df = spark.read \
        .format("jdbc") \
        .option("url", jdbc_url) \
        .option("dbtable", table_name) \
        .option("user", user) \
        .option("password", password) \
        .load()

    # Show sample records
    jdbc_df.show(5)

    # Convert to a DynamicFrame
    glue_df = DynamicFrame.fromDF(jdbc_df, glueContext, f"glue_{table_name}")

    # Define the Glue Catalog sink
    datasink = glueContext.getSink(
        connection_type="s3",
        path=output_s3_path + table_name,
        enableUpdateCatalog=True,
        partitionKeys=[]
    )

    # Set the catalog info to update Glue Data Catalog
    datasink.setCatalogInfo(
        catalogDatabase=glue_database_name,
        catalogTableName=table_name
    )

    # Set output format
    datasink.setFormat("glueparquet")

    # Write the DynamicFrame to S3 and update the Glue Data Catalog
    datasink.writeFrame(glue_df)

    print(f"Data from table '{table_name}' has been written to S3 and updated in the Glue Data Catalog.")