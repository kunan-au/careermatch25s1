import os
from langchain_openai import ChatOpenAI
from sqlalchemy import URL
from langchain.sql_database import SQLDatabase
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain.chains import create_sql_query_chain
from langchain_community.document_loaders import PyPDFLoader
from langchain.output_parsers import CommaSeparatedListOutputParser
from typing import List
import re
from dotenv import load_dotenv

pdf_path = 'Peiyuan_Yu_CV.pdf'

load_dotenv()

def get_recommendations(pdf_path: str)-> List[str]:
    resume = PyPDFLoader(pdf_path).load()
    text_data = ''
    for pg in resume:
        text_data += pg.page_content

    os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')

    llm = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0)
    SQLALCHEMY_DATABASE_URL = URL.create(
        "postgresql",
        username="app",
        password="app",
        host="localhost",
        port=65432,
        database="app",
    )
    db = SQLDatabase.from_uri(SQLALCHEMY_DATABASE_URL)
    execute_query = QuerySQLDataBaseTool(db=db)
    write_query = create_sql_query_chain(llm, db)
    chain = write_query | execute_query
    result = chain.invoke({'question': "Query relevant positions based on the "
                "following resume, extract the skills that job seeker have: \“" + text_data + "\“"
                "query the jobs table in a postgresql database. Your response should be a list of comma separated values, eg: `foo, bar, baz`. Ensure the script uses correct syntax and the output is formatted exactly as shown, including the brackets and quotes. For SQL, generate the SQL query in text without Markdown format, output relevant matching IDs. "
                "You should not always use AND in query."})
    print(result)
    uuids = re.findall(r"UUID\('([a-f\d\-]+)'\)", result)

    # output formatted uuids
    formatted_uuids = [f"{uuid}" for uuid in uuids]
    return formatted_uuids

print(get_recommendations(pdf_path))