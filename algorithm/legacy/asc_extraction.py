from langchain_openai import OpenAIEmbeddings, OpenAI
from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema import HumanMessage, SystemMessage
from pydantic import BaseModel, Field
from typing import List, Dict, Any
import logging
import json

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 常量定义
HR_SYSTEM_MESSAGE = "You are an expert in human resources and skilled at identifying and standardizing skills based on the Australian Skills Classification (ASC)."

# 初始化嵌入模型和Chroma数据库
embeddings = OpenAIEmbeddings()
skill_db = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)

class Skill(BaseModel):
    skill_statement: str
    specialist_task: str

def retrieve_relevant_skills(text: str, k: int = 5) -> List[Dict[str, str]]:
    relevant_skills = skill_db.similarity_search(text, k=k)
    return [{"skill_statement": doc.page_content,
             "specialist_task": doc.metadata['specialist_task']}
            for doc in relevant_skills]

def create_skill_extraction_prompt(text: str, text_type: str, relevant_skills: List[Dict[str, str]]) -> ChatPromptTemplate:
    skills_text = "\n".join(f"Skill Statement: {skill['skill_statement']}\nSpecialist Task: {skill['specialist_task']}"
                            for skill in relevant_skills)
    
    messages = [
        SystemMessage(content=HR_SYSTEM_MESSAGE),
        HumanMessage(content=f"""Please analyze the following {text_type} and identify which of the provided ASC skills are present. 
        Only select skills that are clearly represented in the {text_type}. Do not infer or add skills that are not explicitly mentioned.

        Here are the relevant skills from ASC:

        {skills_text}

        The {text_type} is as follows:

        {text}

        Please list only the identified skills that are present in the {text_type}. Use the exact Skill Statement and Specialist Task as provided. 
        Format your response as a JSON array of objects, each with 'skill_statement' and 'specialist_task' keys.
        If no skills from the provided list match the {text_type}, return an empty array.
        """)
    ]
    
    return ChatPromptTemplate.from_messages(messages)

def extract_skills(llm: Any, text: str, text_type: str) -> List[Skill]:
    relevant_skills = retrieve_relevant_skills(text)
    prompt = create_skill_extraction_prompt(text, text_type, relevant_skills)
    
    chain = (
        {"text": RunnablePassthrough()}
        | prompt
        | llm
    )
    
    result = chain.invoke(text)
    logger.info(f"{text_type} skill extraction result: {result}")
    
    try:
        skills_data = json.loads(result)
        return [Skill(**skill) for skill in skills_data]
    except Exception as e:
        logger.error(f"Error parsing {text_type} skills: {e}")
        return []

def compare_skills(jd_skills: List[Skill], cv_skills: List[Skill]) -> Dict[str, List[str]]:
    matching_tasks = []
    missing_tasks = []

    jd_tasks = {skill.specialist_task for skill in jd_skills}
    cv_tasks = {skill.specialist_task for skill in cv_skills}

    for task in jd_tasks:
        if task in cv_tasks:
            matching_tasks.append(task)
        else:
            missing_tasks.append(task)

    return {
        "matching_skills": matching_tasks,
        "missing_skills": missing_tasks
    }

def match_skills(llm: Any, job_description: str, cv: str) -> Dict[str, List[str]]:
    jd_skills = extract_skills(llm, job_description, "Job Description")
    cv_skills = extract_skills(llm, cv, "CV")
    
    return compare_skills(jd_skills, cv_skills)

# example usage
llm = OpenAI(temperature=0)
job_description = "We are looking for a Python developer with experience in Django and RESTful APIs..."
cv = "Experienced software engineer with 5 years of Python development, including Django and Flask..."
result = match_skills(llm, job_description, cv)
print(result)