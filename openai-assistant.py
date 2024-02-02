import openai
import os
from pathlib import Path
import time

# Decalring the OpenAI client that uses a specific API key
client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# This is the declaration of the assistant that is used to extract the data from the resume
assistant = client.beta.assistants.create(
        name='Resume Editor',
		model='gpt-4-1106-preview',
    	instructions= 'You are a resume analysis and editing assistant. \
             You are skilled in reformatting and editing resumes that are uploaded in the format of .docx and .pdf files. \
             When a resume is uploaded you extract the content from the file, re-edit it to fit into the resume layout that is provided. \
             Your receive the input for the resume format as a JSON file. \
             You strongly stick to the resume format and return the output as a JSON object.',
        tools=[{'type': 'code_interpreter'}]
	)

# This is the declaration of the file that is used to store the resume format
resume_format = client.files.create(
    file=open('data/resume-format.json', 'rb'),
    purpose='assistants')
# This is the declaration of the file from which the resume is extracted
resume_file = client.files.create(
    file=open('data/robert_czanik.docx', 'rb'),
    purpose='assistants')


# This is the declaration of the thread that is used to communicate with the assistant
thread = client.beta.threads.create()
# This is the declaration of the message giving a description of the format layout that is sent to the assistant
message1 = client.beta.threads.messages.create(
    thread_id=thread.id,
    role='user',
    content=f'This is the declarative resume format that you should follow. This format is strict and you should not deviate from it as given in this JSON file. All output should be in this format.',
    file_ids=[resume_format.id])

# This is the declaration of the message which refers to the docx file that is sent to the assistant
message2 = client.beta.threads.messages.create(
    thread_id=thread.id,
    role='user',
    content=f'Extract all of the text from the DOCX file and return it as a JSON object. Return the output as an explicit JSON object in the format defined resume_format file.',
    file_ids=[resume_file.id])


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

print(messages)