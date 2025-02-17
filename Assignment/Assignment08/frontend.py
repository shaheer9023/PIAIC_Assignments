# Required libraries import
import streamlit as st
import os
from PyPDF2 import PdfReader
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

# Streamlit page configuration must be the first Streamlit command
st.set_page_config(
    page_title="PDF AI Assistant",
    page_icon="📚",
    layout="wide"
)

# Load environment variables
load_dotenv()

# Get API key from environment variable
api_key = os.getenv('GOOGLE_API_KEY')

# Enhanced Custom CSS with theme-responsive styling
st.markdown("""
    <style>
    /* Responsive theme-aware styling */
    @media (prefers-color-scheme: dark) {
        .chat-container {
            background: rgba(17, 17, 17, 0.8);
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        }
        
        .user-message {
            background: linear-gradient(135deg, #1a237e 0%, #0d47a1 100%);
            color: white;
        }
        
        .bot-message {
            background: rgba(48, 48, 48, 0.95);
            color: #ffffff;
        }
        
        .file-info-container {
            background: linear-gradient(160deg, #1a237e 0%, #0d47a1 100%);
            color: white;
        }
        
        .header-container {
            background: linear-gradient(160deg, #1a237e 0%, #0d47a1 100%);
        }
        
        .footer {
            background: rgba(17, 17, 17, 0.8);
            color: white;
        }
    }

    @media (prefers-color-scheme: light) {
        .chat-container {
            background: rgba(255, 255, 255, 0.9);
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        }
        
        .user-message {
            background: linear-gradient(135deg, #007CF0 0%, #00DFD8 100%);
            color: white;
        }
        
        .bot-message {
            background: linear-gradient(135deg, #F5F7FA 0%, #E4E9F2 100%);
            color: #333;
        }
        
        .file-info-container {
            background: linear-gradient(160deg, #0093E9 0%, #80D0C7 100%);
            color: white;
        }
        
        .header-container {
            background: linear-gradient(160deg, #0093E9 0%, #80D0C7 100%);
        }
        
        .footer {
            background: rgba(255, 255, 255, 0.9);
            color: #666;
        }
    }

    /* Common styles */
    .chat-container {
        max-width: 800px;
        margin: auto;
        padding: 20px;
        border-radius: 20px;
        backdrop-filter: blur(10px);
    }
    
    .message {
        margin-bottom: 15px;
        padding: 15px 20px;
        border-radius: 20px;
        max-width: 80%;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        animation: fadeIn 0.5s ease-in-out;
    }
    
    .user-message {
        margin-left: auto;
        border: none;
    }
    
    .bot-message {
        margin-right: auto;
        border: none;
        font-size: 1.1rem;
        line-height: 1.6;
    }
    
    .header-container {
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        margin-bottom: 2rem;
        text-align: center;
        color: white;
    }
    
    .header-text {
        font-size: 2.5rem;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
    }
    
    .subheader-text {
        font-size: 1.2rem;
        margin-top: 0.5rem;
        opacity: 0.9;
    }
    
    .file-info-container {
        padding: 1rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
    }
    
    .file-name {
        font-weight: bold;
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
        word-wrap: break-word;
    }
    
    .file-details {
        font-size: 0.9rem;
        opacity: 0.9;
    }
    
    .footer {
        padding: 1rem;
        border-radius: 15px;
        margin-top: 2rem;
        text-align: center;
    }

    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    </style>
""", unsafe_allow_html=True)

# Initialize Gemini AI
@st.cache_resource
def initialize_ai():
    if not api_key:
        st.error("Please set up your Google API key in the .env file")
        st.stop()
    return ChatGoogleGenerativeAI(
        model="gemini-2.0-flash-exp", 
        api_key=api_key
    )

llm = initialize_ai()

# Initialize session state for chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Enhanced header
st.markdown("""
    <div class='header-container'>
        <div class='header-text'>🤖 AI PDF Assistant</div>
        <div class='subheader-text'>Your Intelligent Document Analysis Companion</div>
    </div>
""", unsafe_allow_html=True)

# Enhanced PDF uploader
st.markdown("<div class='upload-container'>", unsafe_allow_html=True)
uploaded_file = st.file_uploader("📄 Upload your PDF file", type=['pdf'])
st.markdown("</div>", unsafe_allow_html=True)

# Sidebar with file information
with st.sidebar:
    if uploaded_file is not None:
        # Get file details
        file_details = {
            "Filename": uploaded_file.name,
            "File size": f"{uploaded_file.size/1024:.1f} KB"
        }
        
        st.markdown("<div class='file-info-container'>", unsafe_allow_html=True)
        st.markdown("<h3>📑 Current File</h3>", unsafe_allow_html=True)
        st.markdown(f"<div class='file-name'>{file_details['Filename']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='file-details'>Size: {file_details['File size']}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='file-info-container'>", unsafe_allow_html=True)
        st.markdown("<h3>📑 No File Uploaded</h3>", unsafe_allow_html=True)
        st.markdown("<div class='file-details'>Please upload a PDF file to get started</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

if uploaded_file is not None:
    # Show loading message
    with st.spinner("Reading PDF..."):
        pdf_reader = PdfReader(uploaded_file)
        document = ""
        for page in pdf_reader.pages:
            document += page.extract_text()
        
        st.success("PDF loaded successfully! You can now ask questions.")

    # Enhanced input field
    cols = st.columns([3, 1])
    with cols[0]:
        user_input = st.text_input(
            "🤔 Ask a question about your PDF:",
            placeholder="Type your question here..."
        )
    with cols[1]:
        submit_button = st.button("🚀 Get Answer", type="primary")

    if submit_button and user_input:
        # Add user message to chat history
        st.session_state.chat_history.append(("user", user_input))
        
        # Show loading state
        with st.spinner("Thinking..."):
            instruction = f"""You are a helpful PDF assistant. Your task is to:
1. Read and understand the following document content
2. Answer the user's question based ONLY on the document content
3. If the question cannot be answered from the document, respond with: "I apologize, but I cannot find information about this in the document."

Document Content: {document}

User Question: {user_input}

Please provide a clear and concise answer."""
            
            try:
                response = llm.invoke(instruction)
                if response and response.content:
                    formatted_response = response.content.replace('•', '◆').replace('*', '★')
                    st.session_state.chat_history.append(("bot", formatted_response))
                else:
                    st.session_state.chat_history.append(("bot", "I apologize, but I encountered an error processing your question. Please try again."))
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                st.session_state.chat_history.append(("bot", "I apologize, but I encountered an error. Please try again."))

    # Display chat history with enhanced styling
    st.markdown("""
        <style>
        .bot-message {
            background: linear-gradient(135deg, #F5F7FA 0%, #E4E9F2 100%);
            color: #333;
            margin-right: auto;
            border: none;
            font-size: 1.1rem;
            line-height: 1.6;
        }
        
        .bot-message ul, .bot-message ol {
            margin-left: 20px;
            margin-top: 10px;
            margin-bottom: 10px;
        }
        
        .bot-message li {
            margin-bottom: 5px;
        }
        
        .bot-message p {
            margin-bottom: 10px;
        }
        
        .highlight {
            background-color: #fff3cd;
            padding: 2px 5px;
            border-radius: 3px;
        }
        </style>
    """, unsafe_allow_html=True)

    # Display chat history
    st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
    for role, message in st.session_state.chat_history:
        if role == "user":
            st.markdown(f"""
                <div class='message user-message'>
                    👤 You: {message}
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div class='message bot-message'>
                    🤖 Assistant: {message}
                </div>
            """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

else:
    # Show instruction when no PDF is uploaded
    st.info("👆 Please upload a PDF file to get started!")

# Enhanced footer
st.markdown("""
    <div class='footer'>
        <p>Created with 💖 by Shaheer Ahmad</p>
        <p style='font-size: 0.8rem;'>Powered by Streamlit & Google Gemini AI</p>
    </div>
""", unsafe_allow_html=True)



