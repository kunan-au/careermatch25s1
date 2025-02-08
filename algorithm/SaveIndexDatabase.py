from dotenv import load_dotenv
import os
import openai
import time
from pinecone import Pinecone, ServerlessSpec
import pandas as pd

load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')
pinecone_api_key = os.getenv('PINECONE_API_KEY')

def embed(text: str) -> list[float]:
    res = openai.embeddings.create(input=text, model="text-embedding-3-large", dimensions=256)
    print(res)
    text_embeds = res.data[0].embedding
    return text_embeds

pc = Pinecone(api_key=pinecone_api_key)

# spec = ServerlessSpec(
#     cloud="aws",
#     region="us-east-1",
# )

# pc.create_index("text-embedding-3-large", dimension=256, metric="dotproduct", spec=spec)
# while not pc.describe_index("text-embedding-3-large").status['ready']:
#     time.sleep(1)

pc_index = pc.Index("text-embedding-3-large")
# time.sleep(1)
# print(pc_index.describe_index_stats())

# # Embed all job descriptions
# def read_csv_as_dict(file_path):
#     df = pd.read_csv(file_path)
#     data = df.to_dict('records')
#     return data

# file_path = 'jobs_table.csv'
# data = read_csv_as_dict(file_path)
# data = list(map(lambda x: {
#     'id': x['id'],
#     'description': x['description'],
#     'metadata': {
#         'title': x['title'],
#         'company': x['company'],
#         'job_type': x['job_type'],
#     }
# }, data))
# print(data)

# batch_size = 100
# for i in range(0, len(data), batch_size):
#     batch = data[i:i+batch_size]
#     for item in batch:
#         item['values'] = embed(item['description'])
#     vectors = [{'id': item['id'], 'values': item['values'], 'metadata': item['metadata']} for item in batch]
#     pc_index.upsert(vectors=vectors)

def get_similar_jobs(resume: str, top_k: int) -> list:
    text_embed = embed(resume)
    res = pc_index.query(vector=text_embed, top_k=top_k, include_metadata=True)
    return res

# Waiting for terminal input
# while True:
# resume = input("Please input your resume: ")
with open('backend_resume.txt', 'r') as file:
    resume = file.read()
top_k = 50
print(get_similar_jobs(resume, top_k))