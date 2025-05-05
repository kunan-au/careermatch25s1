from urllib.parse import quote_plus
import pandas as pd
from sqlalchemy import create_engine

import ast
import json

# Convert 'spacy_entities' from Python dict-string to valid JSON
def fix_json(val):
    try:
        if pd.isna(val):
            return None
        return json.dumps(ast.literal_eval(val))  # convert string dict → real dict → JSON
    except:
        return None  # or handle differently


df = pd.read_csv(r'F:\TechLauncher-S1\job_listings\Processed_JobListing_csv.csv')

user = "admin"
password = quote_plus("123456789")  
host = "database-1.czigki0gmzsn.ap-southeast-2.rds.amazonaws.com"
port = 3306
database = "test_db"

engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}")
df["spacy_entities"] = df["spacy_entities"].apply(fix_json)

df.to_sql(
    'processed_job_descriptions',
    con=engine,
    if_exists='replace',   # <— drops any existing table and creates a new one matching df.columns
    index=False
)


print("✅ Data inserted successfully!")
