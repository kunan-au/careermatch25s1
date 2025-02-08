from langchain.agents import initialize_agent, Tool, tool
from langchain.agents import AgentType
from langchain.tools import BaseTool
from langchain.agents.agent import AgentExecutor
from langchain_openai import ChatOpenAI
from langchain.memory import ChatMessageHistory
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain.agents import create_sql_agent
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from sqlalchemy import create_engine, URL
import os
from dotenv import load_dotenv

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')

# This file is for langchain using.
# ["OPENAI_API_KEY"] will be configured in everyone's env file, not uploaded to the repo


class PositionRecommenderSystem:
    def __init__(self, pdf):
        # Initialize database
        SQLALCHEMY_DATABASE_URL = URL.create(
            "postgresql",
            username="app",
            password="app",
            host="localhost",
            port=65432,
            database="app",
        )

        # db = SQLDatabase.from_uri("postgresql://app:app@localhost:65432/app")
        db = SQLDatabase.from_uri(SQLALCHEMY_DATABASE_URL)

        # Initialize the language model, here we use OpenAI's model
        # May change
        self.lm = ChatOpenAI(temperature=0)

        # Create memory storage
        self.memory = ChatMessageHistory()

        # Initialize resume
        self.resume = None

        # Initialize resume summary
        self.resume_summary = None

        # Initialize loader: text splitter
        # chunk_size and chunk_overlap can be adjusted as needed
        self.text_splitter = CharacterTextSplitter(chunk_size=100, chunk_overlap=20) 


        # Initialize summary chain
        self.summarize_chain = load_summarize_chain(self.lm, chain_type="refine", verbose=False)

        # Initialize database tool
        # tools = [
        #     Tool(
        #         name="Answer",
        #         func=self.answer_dialogue,
        #         description="useful for when you need to answer questions about current dialogue"
        #     )
        # ]
        toolkit = SQLDatabaseToolkit(db=db, llm=self.lm)
        # tools.append(toolkit.get_tools())

        # self.agent = create_sql_agent(
        #     llm=self.lm,
        #     agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        #     toolkit=toolkit,
        #     verbose=True
        # )
        # self.agent = initialize_agent(tools, llm=self.lm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
        self.agent = create_sql_agent(toolkit=toolkit, llm=self.lm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

        # Load Resume
        self.load_pdf_resume(pdf)
        print(self.resume)
        # Update Resume
        self.update_resume(self.resume)

    def load_pdf_resume(self, pdf):
        self.resume = PyPDFLoader(pdf).load()

    # def upload_resume(self, resume):
    #     self.resume = self.text_splitter.create_documents(texts=resume, metadatas=[{"source": "local"}])

    def summarize_resume(self):
        # Split long text resume
        split_documents = self.text_splitter.split_documents(self.resume)
        # Summary Resume Text
        self.resume_summary = self.summarize_chain.run(split_documents)

    def update_resume(self, resume):
        # self.upload_resume(resume=resume)
        self.summarize_resume()
        # Add resume to chat history
        self.memory.add_user_message(self.resume_summary)

        # Resonse
        response = "You have just uploaded your new resume. Here is a summary it: \n" + self.resume_summary
        print(response)
        return response

    def query_positions(self, query):
        # Execute SQL commands through natural language and return the first 10 matching job IDs
        top_positions = self.agent.run(
            "Query relevant positions based on the "
            "following information: \“" + query + "\“"
            "from jobs table, output the most relevant 10 matching IDs? "
            "You should not always use AND in query.")

        return top_positions

    # @tool
    # def answer_dialogue(self, question):
    #     response = self.lm(self.memory.messages)
    #     return response

    def handle_dialogue(self, question):
        # Processing Dialog Output
        self.memory.add_user_message(question)
        # response = self.agent(self.memory.messages)
        response = self.lm(self.memory.messages)
        self.memory.add_ai_message(response.content)
        return response.content

    def recommend_positions(self):
        # Generate job recommendation answers using resume summaries
        question = "Based on the above resume summary, recommend job positions"
        recommendations = self.handle_dialogue(question)
        self.query_positions(recommendations)
        return recommendations


# Example

# resume_text = ""
# with open('Peiyuan_Resume.txt', 'r', encoding='utf-8') as file:
#     resume_text = file.read()
pdf_path = 'Peiyuan_Yu_CV.pdf'
recommender_system = PositionRecommenderSystem(pdf_path)

# recommender_system = PositionRecommenderSystem(resume_text)
print("Here are the recommended positions:")
print(recommender_system.recommend_positions())
# while True:
#     question = input()
#     answer = recommender_system.handle_dialogue(question)
#     print(answer)

# # Example of dialog output
# question = "Can you tell me more about jobs related to data science?"
# print(recommender_system.handle_dialogue(question))
