from urllib.parse import quote_plus
import pandas as pd
from sqlalchemy import create_engine
import ast, json

# ─── Utility to turn Python-style literals into valid JSON strings ───
def fix_json(val):
    try:
        if pd.isna(val):
            return None
        # literal_eval turns "['a','b']" into a Python list, json.dumps → '["a","b"]'
        return json.dumps(ast.literal_eval(val))
    except:
        return None

# ─── 1. Load your processed resumes CSV ────────────────────────────────
resume_csv_path = r'F:\TechLauncher-S1\New folder\Processed_Resumes.csv'  # ← update to your actual path
df = pd.read_csv(resume_csv_path)

# ─── 2. Clean up the JSON-typed columns ────────────────────────────────
for col in ['Persons', 'Orgs', 'Locations']:
    if col in df.columns:
        df[col] = df[col].apply(fix_json)

# ─── 3. Define your DB connection ─────────────────────────────────────
user     = "admin"
password = quote_plus("123456789")   
host     = "database-1.czigki0gmzsn.ap-southeast-2.rds.amazonaws.com"
port     = 3306
database = "test_db"

engine = create_engine(
    f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
)

# ─── 4. Push into MySQL ────────────────────────────────────────────────
df.to_sql(
    'processed_resume',       # table name
    con=engine,
    if_exists='append',
    index=False
)

print("✅ Processed resumes inserted successfully!")
