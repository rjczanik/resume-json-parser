import openai
import os
from pathlib import Path
import time

client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

assistant = client.beta.assistants.create(
        name='Resume Editor',
		model='gpt-4-1106-preview',
    	instructions= 'You are a resume analysis and editing assistant. \
             You are skilled in reformatting and editing resumes that are uploaded in the format of .docx and .pdf files. \
             When a resume is uploaded you extract the content from the file, re-edit it to fit into the resume layout that is provided. \
             You strongly stick to the resume format and return the output as a JSON object.',
        tools=[{'type': 'code_interpreter'}]
	)


# with open('data/resume-format.json') as f:
#     resume_format = f.read()
# open(
#     file=Path('data/resume-format.json'),
#     purpose='fine-tune')

resume_format = client.files.create(
    file=open('data/resume-format.json', 'rb'),
    purpose='assistants')

resume_file = client.files.create(
    file=open('data/robert_czanik.docx', 'rb'),
    purpose='assistants')

thread = client.beta.threads.create()

message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role='user',
    content=f'This is the declarative resume format that you should follow. This format is strict and you should not deviate from it. All output should be in this format.',
    file_ids=[resume_format.id])

message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role='user',
    content=f'Extract all of the text from the DOCX file and return it as a JSON object. Do not give the output as a download link, but give it as text explicitly.',
    file_ids=[resume_file.id])

run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant.id,
    instructions='If there is no text, return a "END" in the JSON response'
)


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

messages = client.beta.threads.messages.list(
    thread_id=thread.id
)

print(messages)

# print("upload of resume format file's results: " + str(results_format) + "\n")
# print("file_id: " + results_format.id)

# results_format = client.fine_tuning.create(training_file=results_format.id, model=config.BASE_MODEL)
# print("fine-tuning results: " + str(results_format) + "\n")
# print("\nUse the following command to check the status of your fine-tuning job:")
# print(f"python openai-chat.py --state {results_format.id}")    

# print("upload of resume docx file's results: " + str(resume_file) + "\n")
# print("file_id: " + results_resume.id)
# results_resume = client.fine_tuning.create(training_file=results_resume.id, model=config.BASE_MODEL)
# print("fine-tuning results: " + str(results_resume) + "\n")
# print("\nUse the following command to check the status of your fine-tuning job:")
# print(f"python openai-chat.py --state {results_resume.id}")    



# # if args.state:
# results = openai.FineTuningJob.retrieve(args.state)
# print('fine-tuning state: ' + str(results)+'\n')