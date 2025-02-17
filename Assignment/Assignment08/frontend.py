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

# Function to get default PDF content
@st.cache_resource
def get_default_content():
    # Yahan pe PDF ka content as a string define kar rahe hain
    return """
    Presidential Initiative for Artificial Intelligence & Computing (PIAIC)
    
    The mission of PIAIC is to reshape Pakistan by revolutionizing education, research, and business by adopting latest, cutting-edge technologies. Experts are calling this the 4th industrial revolution. We want Pakistan to become a global hub for AI, data science, cloud native computing, edge computing, blockchain, augmented reality, and internet of things.
    
    Available Programs:
    1. Artificial Intelligence
    2. Cloud Native and Mobile Web Computing
    3. Blockchain
    4. Internet of Things and AI
    
    Artificial Intelligence Program Details:
    - Duration: 1 Year
    - Learning Tracks: Machine Learning, Deep Learning, AI Applications
    
    Cloud Native Program Details:
    - Duration: 1 Year
    - Learning Tracks: Web Development, Mobile Development, Cloud Computing
    
    Blockchain Program Details:
    - Duration: 1 Year
    - Learning Tracks: Smart Contracts, DApps, Tokenomics
    
    IoT Program Details:
    - Duration: 1 Year
    - Learning Tracks: Embedded Systems, IoT Networks, AI Integration
    """

# Replace PDF loading with static content
document = get_default_content()
st.success("Panaversity content loaded successfully! You can now ask questions.")

# Update sidebar content
with st.sidebar:
    st.markdown("<div class='file-info-container'>", unsafe_allow_html=True)
    st.markdown("<h3>📑 Current Document</h3>", unsafe_allow_html=True)
    st.markdown("<div class='file-name'>Panaversity Content</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

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

    /* Update bot message styling */
    .bot-message {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-left: 4px solid #0093E9;
        padding: 20px;
        font-size: 1.15rem;
        line-height: 1.7;
    }
    
    /* Improve paragraph spacing */
    .bot-message p {
        margin-bottom: 15px;
    }
    
    /* Better list formatting */
    .bot-message ul, .bot-message ol {
        margin: 15px 0;
        padding-left: 25px;
        background: rgba(255,255,255,0.5);
        padding: 15px 30px;
        border-radius: 8px;
    }
    
    .bot-message li {
        margin: 12px 0;
        line-height: 1.6;
        padding-left: 10px;
    }
    
    /* Add section breaks */
    .bot-message hr {
        margin: 20px 0;
        border: 0;
        border-top: 2px solid rgba(0,147,233,0.1);
    }
    
    /* Highlight important points */
    .bot-message strong {
        color: #0093E9;
        font-weight: 600;
        background: rgba(0,147,233,0.1);
        padding: 2px 6px;
        border-radius: 4px;
    }
    
    /* Format headings */
    .bot-message h3 {
        color: #0093E9;
        margin: 20px 0 10px 0;
        font-size: 1.3rem;
    }
    
    /* Add quotes styling */
    .bot-message blockquote {
        border-left: 3px solid #0093E9;
        margin: 15px 0;
        padding: 10px 20px;
        background: rgba(0,147,233,0.05);
        border-radius: 0 8px 8px 0;
    }
    
    /* Add card effect to messages */
    .message {
        transition: transform 0.2s ease;
    }
    
    .message:hover {
        transform: translateY(-2px);
    }
    
    /* Improve code block styling if any */
    .bot-message code {
        background: #f8f9fa;
        padding: 2px 6px;
        border-radius: 4px;
        color: #e83e8c;
        font-family: monospace;
    }
    
    /* Add divider between messages */
    .message {
        position: relative;
        margin-bottom: 25px;
    }
    
    .message::after {
        content: '';
        position: absolute;
        bottom: -12px;
        left: 0;
        right: 0;
        height: 1px;
        background: rgba(0,0,0,0.1);
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
    # Clear previous chat history
    st.session_state.chat_history = []
    
    # Add new user message
    st.session_state.chat_history.append(("user", user_input))
    
    # Show loading state
    with st.spinner("Thinking..."):
        instruction = f"""You are a helpful assistant. Please follow these guidelines:

1. Read and understand the document content carefully
2. Format your response with proper structure:
   - Use headings for different sections
   - Use bullet points or numbered lists for multiple items
   - Add line breaks between paragraphs
   - Highlight important points using **bold** text
3. Answer based ONLY on the document content
4. If information is not in the document, say: "I apologize, but I cannot find this information in the document."

Document Content: {document}

User Question: {user_input}

Please provide a well-structured, clear answer."""
        
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
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-left: 4px solid #0093E9;
        padding: 20px;
        font-size: 1.15rem;
        line-height: 1.7;
    }
    
    /* Improve paragraph spacing */
    .bot-message p {
        margin-bottom: 15px;
    }
    
    /* Better list formatting */
    .bot-message ul, .bot-message ol {
        margin: 15px 0;
        padding-left: 25px;
        background: rgba(255,255,255,0.5);
        padding: 15px 30px;
        border-radius: 8px;
    }
    
    .bot-message li {
        margin: 12px 0;
        line-height: 1.6;
        padding-left: 10px;
    }
    
    /* Add section breaks */
    .bot-message hr {
        margin: 20px 0;
        border: 0;
        border-top: 2px solid rgba(0,147,233,0.1);
    }
    
    /* Highlight important points */
    .bot-message strong {
        color: #0093E9;
        font-weight: 600;
        background: rgba(0,147,233,0.1);
        padding: 2px 6px;
        border-radius: 4px;
    }
    
    /* Format headings */
    .bot-message h3 {
        color: #0093E9;
        margin: 20px 0 10px 0;
        font-size: 1.3rem;
    }
    
    /* Add quotes styling */
    .bot-message blockquote {
        border-left: 3px solid #0093E9;
        margin: 15px 0;
        padding: 10px 20px;
        background: rgba(0,147,233,0.05);
        border-radius: 0 8px 8px 0;
    }
    
    .message {
        transition: transform 0.2s ease;
    }
    
    .message:hover {
        transform: translateY(-2px);
    }
    
    .bot-message code {
        background: #f8f9fa;
        padding: 2px 6px;
        border-radius: 4px;
        color: #e83e8c;
        font-family: monospace;
    }
    
    .message {
        position: relative;
        margin-bottom: 25px;
    }
    
    .message::after {
        content: '';
        position: absolute;
        bottom: -12px;
        left: 0;
        right: 0;
        height: 1px;
        background: rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# Display chat history
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
for role, message in st.session_state.chat_history:
    if role == "user":
        st.markdown(f"""
            <div class='message user-message'>
                👤 <strong>You:</strong> {message}
            </div>
        """, unsafe_allow_html=True)
    else:
        # Convert markdown-style formatting to HTML
        formatted_message = message.replace('*', '<strong>').replace('_', '<em>')
        formatted_message = formatted_message.replace('\n\n', '<br><br>')
        
        st.markdown(f"""
            <div class='message bot-message'>
                🤖 <strong>Assistant:</strong><br><br>
                {formatted_message}
            </div>
        """, unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# Enhanced footer
st.markdown("""
    <div class='footer'>
        <p>Created with 💖 by Shaheer Ahmad</p>
        <p style='font-size: 0.8rem;'>Powered by Streamlit & Google Gemini AI</p>
    </div>
""", unsafe_allow_html=True)



