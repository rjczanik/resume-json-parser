import openai
import os
from pathlib import Path
import sys

# openai.api_key = os.getenv("OPENAI_API_KEY")
# args = sys.argv[1:]

client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


results_format = client.files.create(
    file=Path('data/resume-format.json'),
    purpose='fine-tune')
results_resume = client.files.create(
    file=Path('data/Dataworkz CV Eric Koepke.docx'),
    purpose='fine-tune')
print("upload of resume format file's results: " + str(results_format) + "\n")
print("file_id: " + results_format.id)
results_format = client.fine_tuning.create(training_file=results_format.id, model=config.BASE_MODEL)
print("fine-tuning results: " + str(results_format) + "\n")
print("\nUse the following command to check the status of your fine-tuning job:")
print(f"python openai-chat.py --state {results_format.id}")    

print("upload of resume docx file's results: " + str(results_resume) + "\n")
print("file_id: " + results_resume.id)
results_resume = client.fine_tuning.create(training_file=results_resume.id, model=config.BASE_MODEL)
print("fine-tuning results: " + str(results_resume) + "\n")
print("\nUse the following command to check the status of your fine-tuning job:")
print(f"python openai-chat.py --state {results_resume.id}")    


completion = client.chat.completion.create(
		model='gpt-4-1106-preview',
    	messages= [
            { role: 'system', content: 'You are a resume analysis and editing assistant. \
             You are skilled in reformatting and editing resumes that are uploaded in the format of .docx and .pdf files. \
             When a resume is uploaded you extract the content from the file, re-edit it to fit into the resume layout that is provided. \
             You strongly stick to the resume format and return the output as a JSON object.' },
            { role: 'user', content: 'reformat the resume' }
                ]
	)

# if args.state:
results = openai.FineTuningJob.retrieve(args.state)
print('fine-tuning state: ' + str(results)+'\n')