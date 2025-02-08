import os
from typing import List

import openai
from langchain.chains import create_sql_query_chain
from langchain.sql_database import SQLDatabase
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pinecone import Pinecone
from sqlalchemy import URL


def get_recommendations(pdf_path: str)-> List[str]:
    resume = PyPDFLoader(pdf_path).load()
    text_data = ''
    for pg in resume:
        text_data += pg.page_content

    print(text_data)

    os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')

    llm = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0)
    SQLALCHEMY_DATABASE_URL = URL.create(
        "postgresql",
        username="app",
        password="app",
        host="app_db",
        port=5432,
        database="app",
    )
    db = SQLDatabase.from_uri(SQLALCHEMY_DATABASE_URL)

    system = """You are a {dialect} expert. Given an input question, creat a syntactically correct {dialect} query to run.
    Unless the user specifies in the question a specific number of examples to obtain, query for at most {top_k} results using the LIMIT clause as per {dialect}. You can order the results to return the most informative data in the database.
    Never query for all columns from a table. You must query only the columns that are needed to answer the question. Wrap each column name in double quotes (") to denote them as delimited identifiers.
    Pay attention to use only the column names you can see in the tables below. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.
    Pay attention to use date('now') function to get the current date, if the question involves "today".

    Only use the following tables:
    {table_info}

    Write an initial draft of the query. Then double check the {dialect} query for common mistakes, including:
    - Using NOT IN with NULL values
    - Using UNION when UNION ALL should have been used
    - Using BETWEEN for exclusive ranges
    - Data type mismatch in predicates
    - Properly quoting identifiers
    - Using the correct number of arguments for functions
    - Casting to the correct data type
    - Using the proper columns for joins
    - Not including any Markdown format

    Use format:

    First draft: <<FIRST_DRAFT_QUERY>>
    Final answer: <<FINAL_ANSWER_QUERY>>
    """
    prompt = ChatPromptTemplate.from_messages(
        [("system", system), ("human", "{input}")]
    ).partial(dialect=db.dialect)

    print(prompt)

    def parse_final_answer(output: str) -> str:
        return output.split("Final answer: ")[1]

    execute_query = QuerySQLDataBaseTool(db=db)
    write_query = create_sql_query_chain(llm, db, prompt=prompt)
    chain = write_query | parse_final_answer | execute_query
    result = chain.invoke({'question': 'Recommend 10 most relevant jobs based on skills mentioned in following resume', 'resume' : text_data})
    print(result)
    # uuids = re.findall(r"UUID\('([a-f\d\-]+)'\)", result)

    # # output formatted uuids
    # formatted_uuids = [f"{uuid}" for uuid in uuids]
    # return formatted_uuids

def get_recommendations_2(pdf_path: str)-> List[str]:
    resume = PyPDFLoader(pdf_path).load()
    text_data = ''
    for pg in resume:
        text_data += pg.page_content

    openai.api_key = os.getenv('OPENAI_API_KEY')

    def embed(text: str) -> list[float]:
        res = openai.embeddings.create(input=text, model="text-embedding-3-large", dimensions=256)
        print(res)
        text_embeds = res.data[0].embedding
        return text_embeds

    pc = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))
    pc_index = pc.Index("text-embedding-3-large")

    def get_similar_jobs(resume: str, top_k: int) -> list:
        text_embed = embed(resume)
        res = pc_index.query(vector=text_embed, top_k=top_k, include_metadata=True)
        return res

    top_k = 50
    pc_res = get_similar_jobs(text_data, top_k)
    def extract_ids(data):
    # 初始化一个空列表来存储id值
        id_list = []
        # 检查数据中是否存在'matches'键
        if 'matches' in data:
            # 遍历'matches'中的每个项目
            for item in data['matches']:
                # 提取每个项目的'id'并添加到列表中
                id_list.append(item['id'])
        return id_list
    id_list = extract_ids(pc_res)
    print(id_list)
    return id_list

