import random
import json
import os

# Define fields and skills
fields = {
    "Software Development": ["Python", "Java", "C++", "Git", "Agile"],
    "Data Science": ["Python", "R", "Machine Learning", "SQL", "Statistics"],
    "Marketing": ["SEO", "Content Creation", "Social Media", "Analytics", "CRM"],
    "Finance": ["Excel", "Financial Modeling", "Accounting", "Risk Analysis", "SAP"],
    "Human Resources": ["Recruiting", "Employee Relations", "Payroll", "Compliance", "Training"],
    "Design": ["Adobe Photoshop", "Illustrator", "UI/UX", "Sketch", "Creativity"],
    "Project Management": ["Agile", "Scrum", "Budgeting", "Scheduling", "Risk Management"],
    "Sales": ["Lead Generation", "Negotiation", "CRM", "Customer Relations", "Targets"],
    "Customer Support": ["Communication", "Problem-Solving", "CRM", "Empathy", "Product Knowledge"],
    "Cybersecurity": ["Network Security", "Risk Assessment", "Penetration Testing", "Compliance", "Encryption"]
}

def generate_resumes_and_jobs():
    resumes = []
    job_descriptions = []
    resume_labels = []
    job_labels = []

    # Generate Resume 
    for field, skills in fields.items():
        for i in range(5):  # Generate 5 resumes for each field
            random_skills = random.sample(skills, 3)
            resume = f"{field} professional with experience in {', '.join(random_skills)}."
            resumes.append(resume)
            resume_labels.append(field)  # Store the field label for each resume

    # Generate Job Descriptions
    for field, skills in fields.items():
        for i in range(5):  # Generate 5 job descriptions for each field
            random_skills = random.sample(skills, 3)
            job = f"Looking for a {field} expert skilled in {', '.join(random_skills)}."
            job_descriptions.append(job)
            job_labels.append(field)

    # Ensure the file is saved in the same folder as the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the current script
    file_path = os.path.join(script_dir, 'generated_data.json')  # Set file path in the same directory as the script

    # Save the generated resumes, job descriptions, and labels to a JSON file
    data = {
        "resumes": resumes,
        "job_descriptions": job_descriptions,
        "resume_labels": resume_labels,
        "job_labels": job_labels
    }

    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

    print(f"Data generated and saved to '{file_path}'")

if __name__ == "__main__":
    generate_resumes_and_jobs()
