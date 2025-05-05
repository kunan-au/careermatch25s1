from urllib.parse import quote_plus
import pandas as pd
import re
from sqlalchemy import create_engine
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ─── 1) DB connection setup ─────────────────────────────────────────────
user     = "admin"
password = quote_plus("123456789")
host     = "database-1.czigki0gmzsn.ap-southeast-2.rds.amazonaws.com"
port     = 3306
database = "test_db"

engine = create_engine(
    f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}",
    pool_pre_ping=True,             
    pool_recycle=3600,              # recycle connections every hour
    connect_args={
      "connect_timeout": 10,
      "read_timeout": 3600,         # allow read queries up to 1 hour
      "write_timeout": 3600,
    }
)

# ─── 2) Helpers ─────────────────────────────────────────────────────────
def extract_years(text: str) -> float | None:
    """Extract the first number of years from a string (e.g. '3 years', '5 yrs')."""
    if not isinstance(text, str):
        return None
    m = re.search(r'(\d+(\.\d+)?)\s*(?:\+?years?|yrs?)', text, re.I)
    return float(m.group(1)) if m else None

def determine_weights(title: str) -> tuple[float, float, float]:
    """
    Returns weights (w_general, w_edu, w_exp) based on job seniority:
      - Graduate/Junior roles → more weight on education
      - Senior/Lead/Manager roles → more weight on experience
      - Others → balanced weighting
    """
    t = title.lower()
    if "graduate" in t or "junior" in t:
        return (0.3, 0.7, 0.0)
    elif any(x in t for x in ["senior", "lead", "manager", "principal", "director"]):
        return (0.3, 0.0, 0.7)
    else:
        return (0.5, 0.25, 0.25)

# ─── 3) Matching function with section weights ──────────────────────────
def get_weighted_job_match(resume_id: int, top_n: int = 1) -> pd.DataFrame:
    # Fetch the resume record (all relevant fields)
    resume_df = pd.read_sql(
        f"SELECT Cleaned_Resume, Degrees, Years_of_Experience FROM processed_resume WHERE ID = {resume_id}",
        con=engine
    )
    if resume_df.empty:
        raise ValueError(f"No resume found with ID {resume_id}")

    resume_general = resume_df.at[0, "Cleaned_Resume"] or ""
    resume_edu     = resume_df.at[0, "Degrees"] or ""
    resume_years   = resume_df.at[0, "Years_of_Experience"] or 0.0

    # Fetch all job descriptions with their requirements
    jobs_df = pd.read_sql(
        "SELECT job_id, job_title, company, Cleaned_Description, Required_Experience "
        "FROM processed_job_descriptions",
        con=engine
    )
    jobs_df["Cleaned_Description"].fillna("", inplace=True)
    jobs_df["Required_Experience"].fillna("", inplace=True)

    # Extract numeric required years
    jobs_df["req_years"] = jobs_df["Required_Experience"].apply(extract_years)

    # 1) General TF–IDF similarity
    corpus_gen = [resume_general] + jobs_df["Cleaned_Description"].tolist()
    vec_gen    = TfidfVectorizer(stop_words="english")
    tf_gen     = vec_gen.fit_transform(corpus_gen)
    jobs_df["sim_gen"] = cosine_similarity(tf_gen[0:1], tf_gen[1:]).flatten()

    # 2) Education TF–IDF similarity
    corpus_edu = [resume_edu] + jobs_df["Cleaned_Description"].tolist()
    vec_edu    = TfidfVectorizer(stop_words="english")
    tf_edu     = vec_edu.fit_transform(corpus_edu)
    jobs_df["sim_edu"] = cosine_similarity(tf_edu[0:1], tf_edu[1:]).flatten()

    # 3) Experience similarity (ratio of actual vs required years, capped at 1)
    def sim_exp(req_years: float | None) -> float:
        if req_years is None or req_years == 0:
            return 1.0
        return min(resume_years / req_years, 1.0)

    jobs_df["sim_exp"] = jobs_df["req_years"].apply(sim_exp)

    # 4) Determine weights per job and compute final score
    weights = jobs_df["job_title"].apply(determine_weights)
    jobs_df[["w_gen","w_edu","w_exp"]] = pd.DataFrame(weights.tolist(), index=jobs_df.index)

    jobs_df["final_score"] = (
        jobs_df["sim_gen"] * jobs_df["w_gen"] +
        jobs_df["sim_edu"] * jobs_df["w_edu"] +
        jobs_df["sim_exp"] * jobs_df["w_exp"]
    )

    # Return the top-N matches sorted by final_score
    return jobs_df.sort_values("final_score", ascending=False).head(top_n)[
        ["job_id","job_title","company","final_score"]
    ]

# ─── 4) Example usage ──────────────────────────────────────────────────
if __name__ == "__main__":
    RESUME_ID = 16852973
    top_matches = get_weighted_job_match(RESUME_ID, top_n=3)
    print(f"Top matches for resume {RESUME_ID}:")
    print(top_matches.to_string(index=False))
