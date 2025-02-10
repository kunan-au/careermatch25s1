from langchain import PromptTemplate
from langchain.chains import LLMChain
from langchain_openai import OpenAI
import json

# Initialize OpenAI LLM
llm = OpenAI(temperature=0)

# Define the skill extraction prompt template
skill_extraction_template = """
You are an expert in human resources and you are an expert at matching skills from a job description to a CV of a candidate.

Please extract first the skills from the job description. 
The job description part starts with === 'JOB DESCRIPTION:' === and ends with === 'END JOB DESCRIPTION' ===.
The CV (curriculum vitae of a candidate) description part starts with === CV START: === and ends with === CV END: ===. 

Then output the matching, missing and associated skills using the provided JSON structure.
The matching skills are the skills in the job description part which are also found in the CV (curriculum vitae of a candidate) description part.
The missing skills are those skills which are in the job description part but not in the CV (curriculum vitae of a candidate) description part.
The associated skills are skills related to the job but may not be explicitly mentioned.

Here are some examples of skills that you might find in the job descriptions and CVs:
- Wordpress
- Creating Wordpress websites
- Website Optimization
- PHP
- SQL
- Javascript
- Debugging
- HTML
- HTML5
- CSS
- CSS3
- WOO-Commerce Management
- Client Support
- Python 
- Linux, macOS, and Windows
- Git
- Building E-commerce stores using woocommerce plugin
- Front-end development
- Codeigniter
- Programming languages: C, C++
- Machine Learning
- Deep Learning
- Database: MySQL
- Database: MongoDB
- IDEs: IntelliJ
- Azure Logic apps
- Azure Data Factory
- Azure Functions
- Experience with REST APIs
- Experience with Business Intelligence BI
- Analytical reporting using PowerBI
- Exposure to ITIL

Job Description:
{job_description}

CV:
{cv}

Please output the matching, missing, and associated skills using the following JSON structure:

{{
  "matching_skills": [],
  "missing_skills": [],
  "associated_skills": []
}}

Ensure you only output the JSON format without any additional explanation.
"""

skill_extraction_prompt = PromptTemplate(
    input_variables=["job_description", "cv"],
    template=skill_extraction_template
)

# Create LLMChain for skill extraction
skill_extraction_chain = LLMChain(llm=llm, prompt=skill_extraction_prompt)

# Define the advice prompt template for job seekers
advice_template = """
Based on the following skill analysis:
{skill_analysis}

Please provide 3-5 specific and actionable pieces of advice for the job seeker to improve their suitability for this position. The advice should be concrete, feasible, and directly address the missing skills.

Your response should be in the following format:

1. [First piece of advice]
2. [Second piece of advice]
3. [Third piece of advice]
4. [Fourth piece of advice (if applicable)]
5. [Fifth piece of advice (if applicable)]

Ensure that each piece of advice is clear, specific, and directly related to bridging the gap between the job seeker's current skills and the job requirements.
"""

advice_prompt = PromptTemplate(
    input_variables=["skill_analysis"],
    template=advice_template
)

# Create LLMChain for generating advice
advice_chain = LLMChain(llm=llm, prompt=advice_prompt)

# Define the summary report prompt template for recruiters
summary_template = """
Based on the following skill analysis:
{skill_analysis}

Please provide a concise summary report for the recruiter about the candidate's strengths and weaknesses. The report should include:

1. Candidate's Main Strengths (2-3 points):
   - [Strength 1]
   - [Strength 2]
   - [Strength 3 (if applicable)]

2. Candidate's Main Weaknesses or Areas for Improvement (2-3 points):
   - [Weakness 1]
   - [Weakness 2]
   - [Weakness 3 (if applicable)]

3. Overall Suitability Assessment:
   Provide a percentage (0-100%) indicating how well the candidate's skills match the job requirements. Explain your reasoning for this percentage in one or two sentences.

Please ensure the report is concise, highlighting the most important points. The total length should not exceed 200 words.
"""

summary_prompt = PromptTemplate(
    input_variables=["skill_analysis"],
    template=summary_template
)

# Create LLMChain for generating summary report
summary_chain = LLMChain(llm=llm, prompt=summary_prompt)

def analyze_cv_and_job(job_description, cv):
    # Step 1: Extract skills
    skill_analysis = skill_extraction_chain.invoke({"job_description": job_description, "cv": cv})
    skill_analysis_json = json.loads(skill_analysis['text'])
    
    # Step 2: Generate advice for job seeker
    advice = advice_chain.invoke({"skill_analysis": json.dumps(skill_analysis_json)})
    
    # Step 3: Generate summary report for recruiter
    summary = summary_chain.invoke({"skill_analysis": json.dumps(skill_analysis_json)})
    
    return {
        "skill_analysis": skill_analysis_json,
        "advice_for_job_seeker": advice['text'],
        "summary_for_recruiter": summary['text']
    }

# Usage example
job_description = """=== 'JOB DESCRIPTION:' ===
Senior Full Stack Developer

We are seeking a highly skilled Senior Full Stack Developer to join our dynamic team. The ideal candidate will have a strong background in both front-end and back-end development, with a passion for creating efficient, scalable, and maintainable code.

Required Skills and Experience:
- 5+ years of experience in full stack development
- Proficiency in JavaScript, HTML5, and CSS3
- Strong experience with React.js and Node.js
- Familiarity with database technologies (MySQL, MongoDB)
- Experience with RESTful APIs and microservices architecture
- Knowledge of cloud platforms (AWS or Azure)
- Version control with Git
- Agile development methodologies
- Strong problem-solving and analytical skills
- Excellent communication and teamwork abilities

Nice to Have:
- Experience with TypeScript
- Familiarity with Docker and Kubernetes
- Knowledge of GraphQL
- Experience with CI/CD pipelines
- Understanding of DevOps practices

Responsibilities:
- Develop and maintain web applications using modern JavaScript frameworks
- Collaborate with cross-functional teams to define and implement new features
- Optimize applications for maximum speed and scalability
- Participate in code reviews and contribute to team best practices
- Troubleshoot, debug, and upgrade existing software
- Stay up-to-date with emerging trends and technologies in web development

If you are passionate about creating high-quality software and thrive in a collaborative environment, we want to hear from you!
=== 'END JOB DESCRIPTION' ==="""

cv = """=== CV START: ===
John Doe
Senior Web Developer

Professional Summary:
Dedicated and innovative web developer with 6 years of experience in creating responsive and user-friendly web applications. Proficient in front-end and back-end technologies with a strong focus on JavaScript ecosystems. Committed to writing clean, efficient code and staying updated with the latest industry trends.

Technical Skills:
- Languages: JavaScript (ES6+), HTML5, CSS3, Python
- Front-end: React.js, Vue.js, jQuery, Bootstrap
- Back-end: Node.js, Express.js
- Databases: MySQL, PostgreSQL, MongoDB
- Version Control: Git, GitHub
- APIs: RESTful API design and integration
- Cloud Platforms: Basic AWS experience
- Other: Webpack, Babel, npm, Agile methodologies

Professional Experience:

Web Developer, TechCorp Inc. (2018 - Present)
- Developed and maintained multiple web applications using React.js and Node.js
- Implemented responsive designs ensuring cross-browser compatibility
- Collaborated with UX designers to create intuitive user interfaces
- Integrated third-party APIs and services into existing applications
- Participated in code reviews and mentored junior developers

Junior Web Developer, StartUp Solutions (2016 - 2018)
- Assisted in the development of company websites using HTML, CSS, and JavaScript
- Worked on bug fixing and improving application performance
- Gained experience in Agile development methodologies

Education:
Bachelor of Science in Computer Science, Tech University (2012 - 2016)

Certifications:
- AWS Certified Developer – Associate
- MongoDB Certified Developer

Languages:
- English (Fluent)
- Spanish (Intermediate)

I am passionate about creating efficient, scalable web solutions and continuously improving my skills in full stack development.
=== CV END: ==="""

result = analyze_cv_and_job(job_description, cv)
print(json.dumps(result, indent=2))