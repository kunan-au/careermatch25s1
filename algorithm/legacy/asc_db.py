import pandas as pd
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.schema import Document


# 初始化嵌入模型
embeddings = OpenAIEmbeddings()

def preprocess_skills_data(excel_file_path, sheet_name):
    df = pd.read_excel(excel_file_path, sheet_name)
    
    # 确保所有必要的列都存在
    required_columns = ['Specialist Task', 'Specialist Cluster', 'Cluster Family', 'Skill Statement']
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Required column '{col}' not found in the sheet.")
    
    # 创建文档列表，每个文档包含Skill Statement和相应的元数据
    documents = []
    for _, row in df.iterrows():
        doc = Document(
            page_content=row['Skill Statement'],
            metadata={
                "specialist_task": row['Specialist Task'],
                "specialist_cluster": row['Specialist Cluster'],
                "cluster_family": row['Cluster Family']
            }
        )
        documents.append(doc)
    
    return documents

# 初始化嵌入模型
embeddings = OpenAIEmbeddings()

# # 加载和预处理数据
# df = preprocess_skills_data('/Users/zhongyusi/COMP8715/career-match-vite-fastapi/algorithm/feedback/data/ASC.xlsx','Specialist tasks hierarchy')

# # 使用DataFrameLoader加载数据
# loader = DataFrameLoader(df, page_content_column="combined_text")
# documents = loader.load()

# # 文本分割
# text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
# texts = text_splitter.split_documents(documents)

def build_skill_db(documents, embeddings):
    return Chroma.from_documents(documents, embeddings, persist_directory="./chroma_db")

# 在应用启动时运行
excel_file_path = '/Users/zhongyusi/COMP8715/career-match-vite-fastapi/algorithm/feedback/data/ASC.xlsx'
sheet_name = 'Specialist tasks hierarchy'
documents = preprocess_skills_data(excel_file_path,sheet_name)

# 如果数据库已经存在，直接加载；否则创建新的
import os
if os.path.exists("./chroma_db"):
    skill_db = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)
else:
    skill_db = build_skill_db(documents, embeddings)