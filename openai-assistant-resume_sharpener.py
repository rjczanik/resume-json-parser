import openai
import os
from pathlib import Path
import time

roles=["data engineer", "data scientist", "data architect", "machine learning engineer"]

role = "data architect"
description = "azure"

# Decalring the OpenAI client that uses a specific API key
client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# This is the declaration of the assistant that is used to extract the data from the resume
assistant = client.beta.assistants.create(
        name='Resume Editor',
		model='gpt-4-1106-preview',
    	instructions= f'You are an assistant who helps to improve certain sections of a given resume. \
             You are skilled in reformatting and improving certain sections of a machine learning engineer''s resume that are given to you. \
             The job specs scraped from the website in each prompt are given as HTML files, containing Dutch description of the specific roles. \
             You have to extract the job requirements form the HTML files, translate it to English and change the specific section of the resume for that role. \
             When the resume is uploaded you extract the content from the file, re-edit it and return an improved version of the resume.',
        tools=[{'type': 'code_interpreter'}, {'type': 'retrieval'}],
	)

# This is the declaration of the file containing the resume in JSON format
resume = client.files.create(
    file=open(f'data/resume/resume.json', 'rb'),
    purpose='assistants')


# This is the declaration of the file containing the FRESH-resume JSON format
resume_format = client.files.create(
    file=open(f'data/resume-format.json', 'rb'),
    purpose='assistants')

# This is the declaration of the file containing the job description in HTML elements
job_spec = client.files.create(
    file=open(f'data/jobs/azure-data-architect.html', 'rb'),
    purpose='assistants')

# This is the declaration of the thread that is used to communicate with the assistant
thread = client.beta.threads.create()

# This is the declaration for the prompt that describes the resume in JSON format
prompt_resume = """This is a resume of a machine learning engineer. The resume is in a JSON file given in the FRESH-resume JSON format.
To fully understand the resume I am reffering to the FRESH-resume JSON format, given as another JSON file.
"""

# This is the declaration for the message that is sent to the assistant about the JSON file containing the resume
message_resume = client.beta.threads.messages.create(
    thread_id=thread.id,
    role='user',
    content=prompt_resume,
    file_ids=[resume.id])

# This is the declaration for the prompt that describes the JSON resume 
prompt_resume_format = """
This is a file giving a declaration for the FRESH-resume format as a JSON file."""

# This is the declaration for the message that is sent to the assistant about the JSON file containing the resume
message_format = client.beta.threads.messages.create(
    thread_id=thread.id,
    role='user',
    content=prompt_resume_format,
    file_ids=[resume_format.id])

# This is the declaration for the prompt that is used to describe the section of the resume that is to be improved
# prompt_summary_full = """Reformat the following summary from a machine-learning engineer''s resume into the that for a data engineer: 'I am an experienced machine learning engineer who has worked on numerous data science solutions for multiple companies and clients.
# My main focus is providing end-to-end cloud-based solutions to clients.
# This all is done by doing all the work needed for conceptualizing, developing, and productization of a machine learning solution.
# I also have the certifications to back up my skillset: MLOps, data science, data engineering, and full-stack cloud development.
# My background is in open-source technologies, mainly on the Linux-tech stack.
# Of these technologies I the am strongest in RDMS, Python, R, ETL and the development of data science use cases as web-apps. 
# My most recent experience lies in working as an MLOps engineer, where data science use cases are developed to completion and put into a production state.
# I am also a strong leader with a strategic and entrepreneurial mindset; Enabling me to have also led teams in building solutions using Agile and Scrum.
# As a strong communicator I had no challenge in regular engagements with stakeholders, technical teams, and the delivery team.
# Which also requires me to listen to all parties involved and to understand the problem holisticaly.
# This is done by creating a lateral understanding of a problem and develop the best outcome, and elegant solution for any client.'
# From this summary, a new summary should be created so that it would meet all of the requirements for an azure data architect position extracted from the elements from the uploaded HTML file.
# Only give the new summary, strictly as text output."""

prompt_summary = f"""Reformat the resume for a machine-learning engineer''s resume given in the JSON-file into the that for a {role}.
From the resume given in the FRESH-resume format, a new resume should be created so that it would meet all of the requirements for an azure {role} position extracted from the elements from the uploaded HTML file.
Give the resume for a {role}, in the same FRESH-resume format that the old one for the machine learning engineer was given.
The new resume should be returned in full, and in the format of the FRESH-resume JSON format.
Make sure to provide the complete resume, and not just a summary.
It is very important to give an extensivley revised summary of the role in the field called "brief" in the output JSON file.
Under each work experience, the "highlights" field should strongly focus on the skillset and the experience that is relevant to the role of a {role}.
Please provide the new resume as a downloadable file in the JSON format."""


# This is the declaration of the message which refers to the job spec of the file in its HTML format
message_summary = client.beta.threads.messages.create(
    thread_id=thread.id,
    role='user',
    content=prompt_summary,
    file_ids=[job_spec.id])


# This is the declaration of the run that is used to run the assistant
run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant.id,
    instructions='If there is no text, return a "END" in the JSON response'
)


# This is the declaration of the actual run that is executed by the assistant
start_time = time.time()
while run.status!= "completed":
    run = client.beta.threads.runs.retrieve(
        thread_id=thread.id,
        run_id=run.id
    )
    if run.status in ["failed", "cancelled", "expired", "requires_action"]:
        print(f"run failed: {run.last_error}")
        break

end_time = time.time()

# This is the declaration of the message that is sent to the user and the output delivered.
messages = client.beta.threads.messages.list(
    thread_id=thread.id
)

def get_response(thread):
    return client.beta.threads.messages.list(thread_id=thread.id)

def get_file_ids_from_thread(thread):
    file_ids = [
        file_id
        for m in get_response(thread)
        for file_id in m.file_ids
    ]
    return file_ids

def write_file_to_temp_dir(file_id, output_path):
    file_data = client.files.content(file_id)
    file_data_bytes = file_data.read()
    with open(output_path, "wb") as file:
        file.write(file_data_bytes)

# So to get a file and write it
file_ids = get_file_ids_from_thread(thread)
print(file_ids)
some_file_id = file_ids[0]
write_file_to_temp_dir(some_file_id, f'output/{description}-{role.split(" ")[0]}-{role.split(" ")[1]}-resume.json')

print(messages)
print(f"Time taken: {end_time-start_time}")