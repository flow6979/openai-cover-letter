import openai
import requests
from bs4 import BeautifulSoup
import json
import datetime
import my_secrets
from cover_google_doc import get_google_doc_content
import os

openai.api_key = my_secrets.OPENAI_API_KEY

job_description_url = input("Please enter the job description URL: ")
url_response = requests.get(job_description_url)

html_content = url_response.text

soup = BeautifulSoup(html_content, "html.parser")

job_description = soup.get_text()

job_description = " ".join(job_description.split())

print("Job description successfully retrieved and processed.")

motivation = get_google_doc_content(my_secrets.GOOGLE_DOC_ID)

def get_completion(prompt, model="gpt-3.5-turbo", temperature=0):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,  
    )
    return response.choices[0].message["content"]

delimiter = "####"

extraction_prompt = f"""
Your task is to extract information about the employer, job title, requirements, tasks, 
contact person, and address from the job description marked with {delimiter} characters.

Format your answer as a Python dictionary with "employer", "job title", "requirements", 
"tasks", "contact person", and "address" as keys.

Format the "requirements" and "tasks" as lists.

If the information is missing in the job description, use "unknown" as the value.

Respond as concisely as possible.

Job description: {delimiter}{job_description}{delimiter}
"""

extraction_response_str = get_completion(extraction_prompt)

extraction_response = json.loads(extraction_response_str)

print("Extracted information from job description:")
print(extraction_response)

company_name = job_description_url.split("/")[-2]

save_directory = "saved_job_descriptions"

os.makedirs(save_directory, exist_ok=True)

json_filename = f"{save_directory}/{company_name}.json"

with open(json_filename, "w") as json_file:
    json.dump(extraction_response, json_file)

print(f"Job description saved as {json_filename}")

# Create cover letter
cover_letter_prompt = f"""
Your task is to create a professional cover letter.

Address the letter to the following employer, address, job position, and contact person:
Employer: {extraction_response["employer"]}
Address: {extraction_response["address"]}
Job Position: {extraction_response["job title"]}
Contact Person: {extraction_response["contact person"]}

Use the following sender information:
Name: {my_secrets.name}
Address: {my_secrets.address}
Phone Number: {my_secrets.phone}
Email: {my_secrets.email}

Include the location and date in the letterhead of the cover letter.
Use the location from: {my_secrets.address}
Use the current date in the English date format: {datetime.date.today()}

Describe how the education, work experience, skills, and motivation fulfill 
the job requirements and tasks. Use the following information:
Requirements: {extraction_response["requirements"]}
Tasks: {extraction_response["tasks"]}
Education: {my_secrets.education}
Work Experience: {my_secrets.work_experience}
Skills: {my_secrets.skills}
Motivation: {motivation}

State the salary expectations and possible start date as follows:
Salary Expectations: {my_secrets.salary_expectations}
Possible Start Date: {my_secrets.possible_start_date}

Write in a professional, concise, and compact tone.

Sign the cover letter as {my_secrets.name}.
"""

cover_letter_response = get_completion(cover_letter_prompt, temperature=0.7)