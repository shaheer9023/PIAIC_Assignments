# Google Gemini AI aur PDF reader ke liye libraries import
from PyPDF2 import PdfReader
from langchain_google_genai import ChatGoogleGenerativeAI
import os
# Gemini AI model ko initialize karna with API key
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp", api_key=os.getenv("GEMINI_API_KEY"))

# User se question input lena
user_input = input("Enter your question: ")

# PDF file ka path set karna
pdf_path = "Panaversity Certified Agentic and Robotic AI Engineer.pdf"
pdf_reader = PdfReader(pdf_path)

# PDF se text extract karna
document = ""
for page in pdf_reader.pages:
    document += page.extract_text()

# AI ko instructions dena
instruction = f"""
You have to guide the user according to the provided document.
-the user input is here {user_input}
-the document is here {document}
if user asked something else than the document, you have to say that you are not able to answer that question.
"""

# AI se response lena
response = llm.invoke(instruction)

# Response ko print karna
print(response.content)



