import gradio as gr
from gradio_pdf import PDF
from llama_index.core import (
    StorageContext,
    load_index_from_storage,
    VectorStoreIndex
)

from llama_parse import LlamaParse
import openai
import os
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.openai import OpenAIEmbedding
import chromadb

openai.api_key =openai.api_key = os.getenv("OPENAI_API_KEY")
llmaparse_api_key = os.getenv("LLMAPARSE_API_KEY")

PERSIST_DIR = "./storage"
CHROMA_COLLECTION_NAME = "my_collection"

parser = LlamaParse(api_key=llmaparse_api_key, result_type="markdown")

def match_jobs(cv):
    input_cv = parser.load_data(cv)

    # load from disk
    db = chromadb.PersistentClient(path=PERSIST_DIR)
    chroma_collection = db.get_collection(CHROMA_COLLECTION_NAME)
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    index = VectorStoreIndex.from_vector_store(
        vector_store, embed_model=OpenAIEmbedding()
    )

    query_engine = index.as_query_engine(similarity_top_k=2)  # Retrieve top 2 chunk

    # response = query_engine.query(
    #     f"""You are a brilliant career adviser. Answer a question of job seekers with CV and the job information.\n
    #     If their CV information is given, use that information as well to answer the question.\n
    #     When you respond, please make sure to answer step by step and also show the reference information that you used to answer. \n
    #     If you are not sure about the answer, return NA.\n
    #     You need to show the source nodes that you are using to answer the question at the end of your response.\n
    #     CV: {input_cv}\n
    #     Question: {query}
    #     """
    # )

    # response = query_engine.query(
    # f''' Analyze the given CV against the specific job description for the Senior Data Scientist position at Paxus. Please provide your analysis in the following structure:
    #     1. Matching Skills: Identify and list the skills and experiences in the CV that match the job requirements.\n
    #     2. Missing Skills: Identify and list the job requirements that are not evidently met by the CV.\n
    #     3. Additional Relevant Skills: Highlight any skills or experiences in the CV that, while not explicitly required, could be valuable for this position.\n
    #     4. Actionable Suggestions: Provide 3-5 specific, constructive, and actionable suggestions for the candidate to improve their qualifications for this position.\n
    # Please ensure your analysis is detailed, specific to the given job description and CV, and provides clear, practical advice for the candidate to enhance their eligibility for the Senior Data Scientist position at Paxus.
    # cv: {input_cv}    
    # '''
    # )

    response = query_engine.query(
        f"""Please extract first the skills from the job description. 
        The job description part starts with === 'JOB DESCRIPTION:' === and ends with === 'END JOB DESCRIPTION' ===.
        The CV (curriculum vitae of a candidate) description part starts with === CV START: === and ends with === CV END: ===. 
        Then analyze the given CV against the specific job description for the Senior Data Scientist position at Paxus. Output the matching, missing and associated skills using the provided JSON structure.
        The matching skills are the skills in the job description part which are also found in the CV (curriculum vitae of a candidate) description part.
        The missing skills are those skills which are in the job description part but not in the CV (curriculum vitae of a candidate) description part.
        Additionally, identify any skills or experiences in the CV that, while not explicitly required, could be valuable for this position.
        Finally, provide 3-5 specific, constructive, and actionable suggestions for the candidate to improve their qualifications for this position.

        Here are some examples of skills that you might find in the job descriptions and CVs:
        - Python
        - R
        - SQL
        - Machine Learning
        - Deep Learning
        - Data Visualization
        - Statistical Analysis
        - Big Data Technologies
        - Cloud Platforms (AWS, Azure, GCP)
        - Data Mining
        - Natural Language Processing
        - Predictive Modeling
        - A/B Testing
        - Data Warehousing
        - ETL Processes
        - Spark
        - Hadoop
        - TensorFlow
        - PyTorch
        - Scikit-learn
        - Pandas
        - NumPy
        - Tableau
        - Power BI
        - Git
        - Agile Methodologies

        === 'JOB DESCRIPTION:' ===
        {JOB_DESCRIPTION}
        === 'END JOB DESCRIPTION' ===

        === CV START: ===
        {input_cv}
        === CV END: ===

        Tips: Make sure you answer in the right format using the following JSON structure:

        {{
            "matching_skills": ["skill1", "skill2", ...],
            "missing_skills": ["skill1", "skill2", ...],
            "additional_relevant_skills": ["skill1", "skill2", ...],
            "actionable_suggestions": [
                "suggestion1",
                "suggestion2",
                "suggestion3",
                "suggestion4",
                "suggestion5"
            ]
        }}

        Ensure your analysis is detailed, specific to the given job description and CV, and provides clear, practical advice for the candidate to enhance their eligibility for the Senior Data Scientist position at Paxus.
        """
    )
    
    return response

def main(cv):
    response = match_jobs(cv)
    return response.response

JOB_DESCRIPTION = '''
<b>Title:</b> Senior Data Scientist<br>
<b>Company:</b> Paxus<br>
<b>Location:</b> Sydney, Australia<br>
<b>Description:</b><br>
<b>Key Responsibilities:</b><br>
- Develop and deploy cutting-edge machine learning models, including large language and generative AI models.<br>
- Collaborate with stakeholders to understand business needs and translate them into actionable data solutions.<br>
- Lead and mentor junior data scientists<br>
- Drive the adoption of data-driven decision making across the organisation.<br>
- Stay abreast of the latest advancements in data science and AI.<br>
<b>Skills and Experience:</b><br>
- Extensive experience in data science, with a strong focus on Generative AI.<br>
- Proven experience implementing Generative AI into various programs on an enterprise level<br>
- Proficiency in Python and Machine Learning frameworks<br>
- Deep understanding of natural language processing, computer vision, and other AI techniques e.g. OpenAI<br>
- Strong analytical and problem-solving skills.<br>
- Excellent communication and collaboration skills.<br>
'''

if __name__ == "__main__":
    demo = gr.Interface(
        main,
        [PDF(label="CV")],
        outputs=gr.Textbox(),
        title="Senior Data Scientist - Paxus",
        description=JOB_DESCRIPTION
    )
    demo.launch(debug=True)