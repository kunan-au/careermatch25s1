import json
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_openai import OpenAI 
from langchain_core.output_parsers import StrOutputParser

# --- CRM-173: Define Core Tool Interface & Workflow Template ---

# Initialize LLM (Ensure your OPENAI_API_KEY environment variable is set)
try:
    llm = OpenAI(temperature=0) # Shared 'execution engine' for prompt tools
except Exception as e:
    print(f"Error initializing OpenAI LLM. Ensure API key is set correctly: {e}")
    # Depending on requirements, you might want to exit or handle this differently
    llm = None # Set to None to prevent further errors if initialization fails

# Define the "Tools" (Prompts and potentially other functions)

# Tool 1: Skill Extraction Prompt
skill_extraction_template_str = """
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
    template=skill_extraction_template_str
)
# The "Interface" for this tool: Input=JD, CV; Output=Skill Analysis JSON

# Tool 2: Advice Generation Prompt
advice_template_str = """
Based on the following skill analysis (JSON format):
{skill_analysis_raw}

Please provide 3-5 specific and actionable pieces of advice for the job seeker to improve their suitability for this position. The advice should be concrete, feasible, and directly address the missing skills identified in the analysis.

Your response should be in the following format:

1. [First piece of advice]
2. [Second piece of advice]
3. [Third piece of advice]
4. [Fourth piece of advice (if applicable)]
5. [Fifth piece of advice (if applicable)]

Focus on practical steps the job seeker can take.
"""
advice_prompt = PromptTemplate(
    # Note: Input variable is now the JSON string for skill_analysis
    input_variables=["skill_analysis_raw"],
    template=advice_template_str
)
# The "Interface" for this tool: Input=Skill Analysis JSON String; Output=Advice Text

# Tool 3: Summary Report Prompt
summary_template_str = """
Based on the following skill analysis (JSON format):
{skill_analysis_raw}

Please provide a concise summary report for the recruiter about the candidate's strengths and weaknesses relative to the job description. The report should include:

1. Candidate's Main Strengths based on Matching Skills (2-3 points):
   - [Strength 1]
   - [Strength 2]
   - [Strength 3 (if applicable)]

2. Candidate's Main Weaknesses or Gaps based on Missing Skills (2-3 points):
   - [Weakness 1]
   - [Weakness 2]
   - [Weakness 3 (if applicable)]

3. Overall Suitability Assessment:
   Provide a percentage (0-100%) indicating how well the candidate's skills match the job requirements based *only* on the provided skill analysis. Explain your reasoning for this percentage in one sentence.

Ensure the report is concise and directly derived from the skill analysis. Maximum 150 words.
"""
summary_prompt = PromptTemplate(
    # Note: Input variable is now the JSON string for skill_analysis
    input_variables=["skill_analysis_raw"],
    template=summary_template_str
)
# The "Interface" for this tool: Input=Skill Analysis JSON String; Output=Summary Text

# Tool 4: Input Validator (Example of a non-prompt 'tool')
def validate_inputs(job_description, cv):
    """Simple validation tool."""
    if not job_description or not isinstance(job_description, str) or len(job_description.strip()) == 0 :
        raise ValueError("Job description must be a non-empty string.")
    if not cv or not isinstance(cv, str) or len(cv.strip()) == 0:
        raise ValueError("CV must be a non-empty string.")
    print("Tool 'validate_inputs': Inputs are valid.")
    return True # Or return validated/cleaned data if needed

# Tool 5: JSON Parser (Helper Tool)
def parse_json_string(json_string):
    """Parses a JSON string into a Python dictionary."""
    try:
        return json.loads(json_string)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        print(f"Problematic JSON string: {json_string[:500]}...") # Print start of string for debugging
        raise ValueError("Skill analysis result was not valid JSON.") from e


# Define the "Workflow Template" - Represents *potential* steps
SKILL_ANALYSIS_WORKFLOW_TEMPLATE = [
    {"step_id": "validate", "tool_type": "function", "tool": validate_inputs, "inputs": ["job_description", "cv"]}, # Common Step 1
    {"step_id": "extract_skills", "tool_type": "prompt_chain", "name": "skill_extraction", "prompt": skill_extraction_prompt, "inputs": ["job_description", "cv"], "output_key": "skill_analysis_raw"}, # Common Step 2
    {"step_id": "parse_skills", "tool_type": "processing", "function": parse_json_string, "inputs": ["skill_analysis_raw"], "output_key": "skill_analysis_json"}, # Common Step 3
    {"step_id": "generate_advice", "tool_type": "prompt_chain", "name": "advice_generation", "prompt": advice_prompt, "inputs": ["skill_analysis_raw"], "output_key": "advice_text", "roles": ["job_seeker"]}, # Role specific - Takes RAW JSON string
    {"step_id": "generate_summary", "tool_type": "prompt_chain", "name": "summary_generation", "prompt": summary_prompt, "inputs": ["skill_analysis_raw"], "output_key": "summary_text", "roles": ["recruiter"]}     # Role specific - Takes RAW JSON string
]
# print("--- CRM-173: Tools and Workflow Template Defined (Supporting Roles) ---")

# --- CRM-174: Implement Role-Based Workflow Execution Engine ---

def execute_skill_analysis_workflow(job_description, cv, user_role):
    """
    Executes the skill analysis workflow based on the user's role.
    Selectively runs steps from the template.
    """
    if llm is None:
      raise RuntimeError("OpenAI LLM failed to initialize. Cannot execute workflow.")

    # print(f"\n--- CRM-174: Starting Workflow Execution for Role: {user_role} ---")
    if user_role not in ["recruiter", "job_seeker"]:
        raise ValueError("Invalid user_role specified. Must be 'recruiter' or 'job_seeker'.")

    workflow_context = {
        "job_description": job_description,
        "cv": cv
    }
    final_output = {} # Initialize dictionary for role-specific final results

    for step in SKILL_ANALYSIS_WORKFLOW_TEMPLATE:
        step_id = step["step_id"]
        # Check if the step is applicable for the current user role
        applicable_roles = step.get("roles")
        if applicable_roles and user_role not in applicable_roles:
            print(f"Skipping step '{step_id}' - Not applicable for role '{user_role}'.")
            continue # Skip this step

        # Proceed with execution if role matches or if no roles are specified (common step)
        tool_type = step["tool_type"]
        # Prepare inputs based on the 'inputs' keys defined in the template step
        try:
            inputs = {input_key: workflow_context[input_key] for input_key in step["inputs"]}
        except KeyError as e:
            print(f"Error preparing inputs for step '{step_id}'. Missing key in context: {e}")
            raise RuntimeError(f"Workflow context error at step '{step_id}'") from e

        output_key = step.get("output_key")

        print(f"Executing step: '{step_id}' for role '{user_role}'")

        try:
            result = None # Initialize result for the step
            if tool_type == "function":
                result = step["tool"](**inputs) # Call the function directly
            elif tool_type == "prompt_chain":
                try:
                    runnable_chain = step["prompt"] | llm | StrOutputParser()
                    result = runnable_chain.invoke(inputs)
                except Exception as chain_error:
                    print(f"Error invoking LCEL chain for step '{step_id}': {chain_error}")
                    raise chain_error
            elif tool_type == "processing":
                 # Assumes single input key for processing functions like json.loads
                input_key_for_processing = step["inputs"][0]
                result = step["function"](inputs[input_key_for_processing])
            else:
                 print(f"Warning: Unknown tool_type '{tool_type}' for step '{step_id}'")

            # Store result in context if an output key is defined
            if output_key:
                workflow_context[output_key] = result
                # print(f"  Stored '{output_key}' in context.") # Optional debug print

        except Exception as e:
            print(f"Error executing step '{step_id}' for role '{user_role}': {e}")
            # Consider more granular error handling here if needed
            raise # Stop the flow on error

    # print(f"--- CRM-174: Workflow Execution Finished for Role: {user_role} ---")

    # Construct the final output based on the role and available context
    if "skill_analysis_json" in workflow_context:
        final_output["skill_analysis"] = workflow_context["skill_analysis_json"]
    else:
        # This shouldn't happen if the workflow ran correctly, but good to check
        print("Warning: 'skill_analysis_json' not found in context after workflow completion.")

    if user_role == "recruiter":
        if "summary_text" in workflow_context:
            final_output["summary_for_recruiter"] = workflow_context["summary_text"]
        else:
             print("Warning: 'summary_text' not found in context for recruiter role.")
    elif user_role == "job_seeker":
        if "advice_text" in workflow_context:
             final_output["advice_for_job_seeker"] = workflow_context["advice_text"]
        else:
             print("Warning: 'advice_text' not found in context for job_seeker role.")


    return final_output

# --- CRM-175: Finalize Role-Specific Output & Validation Stub ---

def validate_final_output(analysis_result, user_role):
    """
    Validates the structure of the final output based on the user role
    that generated it. Acts as a "Test Execution Stub".
    """
    # print(f"\n--- CRM-175: Validating Final Output Structure for Role: {user_role} ---")
    is_valid = True
    if not isinstance(analysis_result, dict):
        print("Error: Final output is not a dictionary.")
        return False

    # Define expected keys based on role
    if user_role == "recruiter":
        expected_keys = ["skill_analysis", "summary_for_recruiter"]
    elif user_role == "job_seeker":
        expected_keys = ["skill_analysis", "advice_for_job_seeker"]
    else:
        print(f"Error: Unknown user_role '{user_role}' for validation.")
        return False

    # Check presence of expected keys
    missing_keys = []
    for key in expected_keys:
        if key not in analysis_result:
            missing_keys.append(key)
            is_valid = False
    if missing_keys:
        print(f"Error: Missing expected key(s) {missing_keys} for role '{user_role}'.")


    # Basic type checks for present keys
    if "skill_analysis" in analysis_result and not isinstance(analysis_result["skill_analysis"], dict):
         print("Error: 'skill_analysis' should be a dictionary, but found", type(analysis_result["skill_analysis"]))
         is_valid = False
    if "summary_for_recruiter" in analysis_result and not isinstance(analysis_result["summary_for_recruiter"], str):
         print("Error: 'summary_for_recruiter' should be a string, but found", type(analysis_result["summary_for_recruiter"]))
         is_valid = False
    if "advice_for_job_seeker" in analysis_result and not isinstance(analysis_result["advice_for_job_seeker"], str):
         print("Error: 'advice_for_job_seeker' should be a string, but found", type(analysis_result["advice_for_job_seeker"]))
         is_valid = False

    if is_valid:
        print(f"Final output structure is valid for role '{user_role}'.")
    else:
        print(f"Final output structure is invalid for role '{user_role}'.")
    return is_valid

# --- Example Usage (Demonstrating role-based calls and validation) ---

# ** REPLACE WITH YOUR ACTUAL EXAMPLE JOB DESCRIPTION AND CV TEXT **
job_description_example = """=== 'JOB DESCRIPTION:' ===
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
=== 'END JOB DESCRIPTION' ==="""

cv_example = """=== CV START: ===
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
- Cloud Platforms: Basic AWS experience (AWS Certified Developer – Associate)
- Other: Webpack, Babel, npm, Agile methodologies
=== CV END: ==="""

if __name__ == "__main__":
    if llm is None:
        print("Cannot run examples because LLM failed to initialize.")
    else:
        # --- Run for Recruiter ---
        try:
            print("\n\n======= EXECUTING FOR RECRUITER =======")
            recruiter_result = execute_skill_analysis_workflow(job_description_example, cv_example, user_role="recruiter")
            recruiter_result_json = json.dumps(recruiter_result, indent=2)
            print("\n--- CRM-175: Recruiter Final Output (JSON) ---")
            print(recruiter_result_json)
            validate_final_output(recruiter_result, user_role="recruiter")
        except Exception as e:
            print(f"\nRecruiter workflow failed: {e}")
            # Optionally print traceback for debugging
            # import traceback
            # traceback.print_exc()

        # --- Run for Job Seeker ---
        try:
            print("\n\n======= EXECUTING FOR JOB SEEKER =======")
            job_seeker_result = execute_skill_analysis_workflow(job_description_example, cv_example, user_role="job_seeker")
            job_seeker_result_json = json.dumps(job_seeker_result, indent=2)
            print("\n--- CRM-175: Job Seeker Final Output (JSON) ---")
            print(job_seeker_result_json)
            validate_final_output(job_seeker_result, user_role="job_seeker")
        except Exception as e:
            print(f"\nJob Seeker workflow failed: {e}")
            # Optionally print traceback for debugging
            # import traceback
            # traceback.print_exc()