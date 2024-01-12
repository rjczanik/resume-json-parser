from langchain.document_loaders import PyPDFLoader
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
import os

#Locate your PDF here.
pdf="data/resume-robert.pdf"
#Load the PDF
loader = PyPDFLoader(pdf)
documents = loader.load()

api_key = os.environ.get("OPENAI_API_KEY")
llm = OpenAI(openai_api_key=api_key)
chain = load_qa_chain(llm,verbose=True)
question = input("Enter your question here : ")
response = chain.run(input_documents=documents, question=question)
print(response) 