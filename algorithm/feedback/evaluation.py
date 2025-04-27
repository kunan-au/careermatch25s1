from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score, recall_score, f1_score
import numpy as np
import openai
import os
import json

# Setting the OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

# # Simulated resume dataset
# resumes = [
#     "Software engineer with 5 years of experience in Java and Python. Skilled in backend development and database design.",
#     "Data analyst with expertise in Python, R, and SQL. Experienced in data visualization and machine learning models.",
#     "Full-stack developer proficient in React, Node.js, and MongoDB. Strong knowledge in web development.",
#     "Marketing manager with over 10 years of experience in digital marketing, SEO, and content creation.",
#     "DevOps engineer experienced in Docker, Kubernetes, CI/CD pipelines, and cloud services."
# ]

# # Simulated job description dataset
# job_descriptions = [
#     "Looking for a software engineer with strong experience in backend development, Java, and Python.",
#     "Hiring a data analyst with skills in Python, SQL, and machine learning techniques.",
#     "We need a full-stack developer skilled in React and Node.js, with strong knowledge in web application development.",
#     "Seeking a marketing manager with expertise in digital marketing, SEO, and content strategies.",
#     "Hiring a DevOps engineer proficient in Docker, Kubernetes, and cloud infrastructure."
# ]

# # True Match Label (1 means match, 0 means no match)
# matching_labels = [
#     [1, 0, 0, 0, 0],  # 简历1 -> 职位1
#     [0, 1, 0, 0, 0],  # 简历2 -> 职位2
#     [0, 0, 1, 0, 0],  # 简历3 -> 职位3
#     [0, 0, 0, 1, 0],  # 简历4 -> 职位4
#     [0, 0, 0, 0, 1]   # 简历5 -> 职位5
# ]


# Load the data from JSON
with open('generated_data.json', 'r') as f:
    data = json.load(f)

resumes = data["resumes"]
job_descriptions = data["job_descriptions"]
resume_labels = data["resume_labels"]
job_labels = data["job_labels"]

# Generate True Match Labels
matching_labels = []

for resume_label in resume_labels:
    row = []
    for job_label in job_labels:
        if resume_label == job_label:
            row.append(1)  # Match
        else:
            row.append(0)  # No match
    matching_labels.append(row)

matching_labels = np.array(matching_labels)

# 1. use all-mpnet-base-v2 model
mpnet_model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')

# generate resume and job description embeddings (MPNet)
resume_vectors_mpnet = mpnet_model.encode(resumes)
job_vectors_mpnet = mpnet_model.encode(job_descriptions)

# calculate cosine similarity of MPNet embeddings
similarities_mpnet = cosine_similarity(resume_vectors_mpnet, job_vectors_mpnet)

# 2. use distilbert-base-nli-stsb-mean-tokens model
distilbert_model = SentenceTransformer('sentence-transformers/distilbert-base-nli-stsb-mean-tokens')

# generate resume and job description embeddings (DistilBERT)
resume_vectors_distilbert = distilbert_model.encode(resumes)
job_vectors_distilbert = distilbert_model.encode(job_descriptions)

# calculate cosine similarity of DistilBERT embeddings
similarities_distilbert = cosine_similarity(resume_vectors_distilbert, job_vectors_distilbert)

# 3. use all-MiniLM-L6-v2 model
minilm_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# generate resume and job description embeddings (MiniLM)
resume_vectors_minilm = minilm_model.encode(resumes)
job_vectors_minilm = minilm_model.encode(job_descriptions)

# calculate cosine similarity of MiniLM embeddings
similarities_minilm = cosine_similarity(resume_vectors_minilm, job_vectors_minilm)

# # 3. use OpenAI text-embedding-ada-002 model
# def get_embeddings_openai(text):
#     response = openai.embeddings.create(
#         model="text-embedding-ada-002",
#         input=[text]
#     )
#     return np.array(response.data[0].embedding)

# # generate resume and job description embeddings (OpenAI)
# resume_vectors_openai = [get_embeddings_openai(resume) for resume in resumes]
# job_vectors_openai = [get_embeddings_openai(job) for job in job_descriptions]

# # calculate cosine similarity of OpenAI embeddings
# similarities_openai = cosine_similarity(resume_vectors_openai, job_vectors_openai)

# 4. use OpenAI text-embedding-ada-002 model with batch processing
def get_embeddings_openai(texts, batch_size=10):
    all_embeddings = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i+batch_size]
        response = openai.embeddings.create(input=batch, model="text-embedding-ada-002")
        embeddings = [np.array(item.embedding) for item in response.data]
        all_embeddings.extend(embeddings)
    return all_embeddings

#  generate resume and job description embeddings (OpenAI)
resume_vectors_openai = get_embeddings_openai(resumes, batch_size=5)
job_vectors_openai = get_embeddings_openai(job_descriptions, batch_size=5)

# calculate cosine similarity of OpenAI embeddings
similarities_openai = cosine_similarity(resume_vectors_openai, job_vectors_openai)


# 5. set the threshold for recommendation
threshold_mpnet = 0.75
threshold_distilbert = 0.75
threshold_openai = 0.9 
threshold_minilm = 0.75

# based on the cosine similarity, recommend the job description for each resume
recommendations_mpnet = [[1 if sim >= threshold_mpnet else 0 for sim in row] for row in similarities_mpnet]
recommendations_distilbert = [[1 if sim >= threshold_distilbert else 0 for sim in row] for row in similarities_distilbert]
recommendations_openai = [[1 if sim >= threshold_openai else 0 for sim in row] for row in similarities_openai]
recommendations_minilm = [[1 if sim >= threshold_minilm else 0 for sim in row] for row in similarities_minilm]

# 6. print the recommendations
for i, label in enumerate(matching_labels):
    print(f"Resume {i+1}:")
    print(f"MPNet Recommended: {recommendations_mpnet[i]}, True Label: {label}")
    print(f"DistilBERT Recommended: {recommendations_distilbert[i]}, True Label: {label}")
    print(f"OpenAI Recommended: {recommendations_openai[i]}, True Label: {label}")
    print(f"MiniLM Recommended: {recommendations_minilm[i]}, True Label: {label}")
    print()

# calculate the accuracy of the models
# mpnet_accuracy = accuracy_score([max(row) for row in matching_labels], [max(row) for row in recommendations_mpnet])
# distilbert_accuracy = accuracy_score([max(row) for row in matching_labels], [max(row) for row in recommendations_distilbert])
# openai_accuracy = accuracy_score([max(row) for row in matching_labels], [max(row) for row in recommendations_openai])
# minilm_accuracy = accuracy_score([max(row) for row in matching_labels], [max(row) for row in recommendations_minilm])

# print(f"MPNet Accuracy: {mpnet_accuracy}")
# print(f"DistilBERT Accuracy: {distilbert_accuracy}")
# print(f"OpenAI Accuracy: {openai_accuracy}")
# print(f"MiniLM Accuracy: {minilm_accuracy}")


def evaluate_model(recommendations, labels):
    y_true = np.array(labels).flatten()
    y_pred = np.array(recommendations).flatten()
    precision = precision_score(y_true, y_pred)
    recall = recall_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred)
    return precision, recall, f1

# evaluate the models
precision_mpnet, recall_mpnet, f1_mpnet = evaluate_model(recommendations_mpnet, matching_labels)
precision_distilbert, recall_distilbert, f1_distilbert = evaluate_model(recommendations_distilbert, matching_labels)
precision_openai, recall_openai, f1_openai = evaluate_model(recommendations_openai, matching_labels)
precision_minilm, recall_minilm, f1_minilm = evaluate_model(recommendations_minilm, matching_labels)

print(f"MPNet - Precision: {precision_mpnet}, Recall: {recall_mpnet}, F1-score: {f1_mpnet}")
print(f"DistilBERT - Precision: {precision_distilbert}, Recall: {recall_distilbert}, F1-score: {f1_distilbert}")
print(f"OpenAI - Precision: {precision_openai}, Recall: {recall_openai}, F1-score: {f1_openai}")
print(f"MiniLM - Precision: {precision_minilm}, Recall: {recall_minilm}, F1-score: {f1_minilm}")


### test1 Output:
# Resume 1:
# MPNet Recommended: [1, 0, 0, 0, 0], True Label: [1, 0, 0, 0, 0]
# DistilBERT Recommended: [1, 0, 0, 0, 0], True Label: [1, 0, 0, 0, 0]
# OpenAI Recommended: [1, 1, 1, 0, 1], True Label: [1, 0, 0, 0, 0]
# MiniLM Recommended: [1, 0, 0, 0, 0], True Label: [1, 0, 0, 0, 0]

# Resume 2:
# MPNet Recommended: [0, 0, 0, 0, 0], True Label: [0, 1, 0, 0, 0]
# DistilBERT Recommended: [0, 1, 0, 0, 0], True Label: [0, 1, 0, 0, 0]
# OpenAI Recommended: [1, 1, 0, 1, 0], True Label: [0, 1, 0, 0, 0]
# MiniLM Recommended: [0, 1, 0, 0, 0], True Label: [0, 1, 0, 0, 0]

# Resume 3:
# MPNet Recommended: [0, 0, 1, 0, 0], True Label: [0, 0, 1, 0, 0]
# DistilBERT Recommended: [0, 0, 1, 0, 0], True Label: [0, 0, 1, 0, 0]
# OpenAI Recommended: [1, 1, 1, 1, 1], True Label: [0, 0, 1, 0, 0]
# MiniLM Recommended: [0, 0, 1, 0, 0], True Label: [0, 0, 1, 0, 0]

# Resume 4:
# MPNet Recommended: [0, 0, 0, 0, 0], True Label: [0, 0, 0, 1, 0]
# DistilBERT Recommended: [0, 0, 0, 0, 0], True Label: [0, 0, 0, 1, 0]
# OpenAI Recommended: [0, 0, 0, 1, 0], True Label: [0, 0, 0, 1, 0]
# MiniLM Recommended: [0, 0, 0, 1, 0], True Label: [0, 0, 0, 1, 0]

# Resume 5:
# MPNet Recommended: [0, 0, 0, 0, 1], True Label: [0, 0, 0, 0, 1]
# DistilBERT Recommended: [0, 0, 0, 0, 1], True Label: [0, 0, 0, 0, 1]
# OpenAI Recommended: [1, 1, 1, 1, 1], True Label: [0, 0, 0, 0, 1]
# MiniLM Recommended: [0, 0, 0, 0, 1], True Label: [0, 0, 0, 0, 1]

# MPNet Accuracy: 0.6
# DistilBERT Accuracy: 0.8
# OpenAI Accuracy: 1.0


# test2 Output:
# MPNet - Precision: 1.0, Recall: 0.856, F1-score: 0.9224137931034483
# DistilBERT - Precision: 0.9545454545454546, Recall: 0.672, F1-score: 0.7887323943661971
# OpenAI - Precision: 1.0, Recall: 0.864, F1-score: 0.9270386266094421
# MiniLM - Precision: 1.0, Recall: 0.728, F1-score: 0.8425925925925926

# MPNet Accuracy: 0.98
# DistilBERT Accuracy: 0.98
# OpenAI Accuracy: 1.0
# MiniLM Accuracy: 0.96
# MPNet - Precision: 1.0, Recall: 0.896, F1-score: 0.9451476793248946
# DistilBERT - Precision: 0.9709302325581395, Recall: 0.668, F1-score: 0.7914691943127962
# OpenAI - Precision: 1.0, Recall: 0.88, F1-score: 0.9361702127659575
# MiniLM - Precision: 1.0, Recall: 0.676, F1-score: 0.8066825775656324
