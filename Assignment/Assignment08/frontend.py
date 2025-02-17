# Google Gemini AI aur PDF reader ke liye libraries import
from PyPDF2 import PdfReader
from langchain_google_genai import ChatGoogleGenerativeAI
import streamlit as st
from dotenv import load_dotenv
import os
from os import getenv

# Load environment variables
load_dotenv()

# Page config and styling
st.set_page_config(
    page_title="AI PDF Assistant",
    page_icon="📚",
    layout="centered"
)

# Custom CSS
st.markdown("""
    <style>
    .stTextInput {
        max-width: 800px;
    }
    .main {
        padding: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# Header section
st.title("🤖 AI PDF Assistant")


# Initialize Gemini AI
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-exp", 
    api_key=os.getenv("GOOGLE_API_KEY")
)

# Sidebar for PDF info
with st.sidebar:
    st.header("📄 Document Info")
    st.info("Currently loaded: Panaversity Certified Agentic and Robotic AI Engineer.pdf")

# Main chat interface
st.markdown("### Ask anything about the document 💭")
user_input = st.text_input("", placeholder="Enter your question here...")

# PDF processing
pdf_path = "Panaversity Certified Agentic and Robotic AI Engineer.pdf"
pdf_reader = PdfReader(pdf_path)

document = ""
for page in pdf_reader.pages:
    document += page.extract_text()

# Process query when user inputs something
if user_input:
    with st.spinner("AI is thinking..."):
        instruction = f"""
        You have to guide the user according to the provided document.
        -the user input is here {user_input}
        -the document is here {document}
        if user asked something else than the document like,(hello or what is your name love you miss you etc blaa blaa type silly questions )
        you have to judge the question and if the question is not related to the document then you have to say that you are not able to answer that question but if the question is related to the document then you have to answer the question.
        """
        
        response = llm.invoke(instruction)
        
        # Display response in a nice container
        st.markdown("### Response:")
        st.write(response.content)

# Footer
st.markdown("---")
st.markdown("*Built with ♥ by Shaheer Ahmad* 🚀")



