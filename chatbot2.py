import os
from dotenv import load_dotenv
import streamlit as st
import time
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Load environment variables
load_dotenv()

# Set up environment variables
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"

# Define the prompt template
prompts = ChatPromptTemplate.from_messages(
    [("user", "Question: {question}")]
)

# LLM setup
llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.7)
output_parser = StrOutputParser()
chain = prompts | llm | output_parser

# Custom CSS
def load_css():
    st.markdown("""
        <style>
            .stApp {
                background-color: #ffffff;
                color: #333333;
            }
            .chat-container {
                background-color: #f8f9fa;
                border-radius: 10px;
                padding: 20px;
                margin: 10px 0;
                border: 1px solid #e9ecef;
            }
            .user-input {
                background-color: #ffffff;
                border-radius: 5px;
                border: 1px solid #ced4da;
                padding: 10px;
                color: #333333;
                width: 100%;
            }
            .sidebar .sidebar-content {
                background-color: #f8f9fa;
            }
            .stButton>button {
                background-color: #0d6efd;
                color: white;
                border-radius: 5px;
                padding: 10px 20px;
                border: none;
                width: 100%;
            }
            .stButton>button:hover {
                background-color: #0b5ed7;
            }
        </style>
    """, unsafe_allow_html=True)

def send_message():
    """Function to send user message when 'Enter' is pressed or 'Send' button is clicked."""
    user_input_value = st.session_state.get("user_input", "").strip()
    
    if user_input_value:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_input_value})
        
        # Get AI response
        with st.spinner("Thinking..."):
            try:
                response = chain.invoke({"question": user_input_value})
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"An error occurred: {e}")
        
        # Clear input field
        st.session_state.user_input = ""
        #st.rerun()

def main():
    # Set page configuration
    st.set_page_config(
        page_title="GeminiSpark",
        page_icon="💬",
        layout="wide"
    )
    
    load_css()
    
    # Sidebar
    with st.sidebar:
        st.title("GeminiSpark")
        st.markdown("---")
        if st.button("+ New Chat"):
            st.session_state.messages = []

    # Main title and description
    st.markdown("<h1 style='text-align: center;'>GeminiSpark</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>Hints at quick and insightful responses</h3>", unsafe_allow_html=True)

    # Footer
    st.markdown(
        """
        <div style="text-align: center; font-size: 16px;">
            🛠️ <b style="color: #2196F3;">Developed by RK</b> |
            ✅ <b style="color: #4CAF50;">Powered by Gemini Pro, LangChain & FAISS</b> |
            🚀 <b style="color: #FF9800;">Built with Streamlit</b>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    st.markdown("<h3 style='text-align: center;'>Ask anything and get responses powered by Google Gemini!</h3>", unsafe_allow_html=True)
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages
    for message in st.session_state.messages:
        with st.container():
            st.markdown(f"""
                <div class="chat-container">
                    <b>{'User' if message['role'] == 'user' else 'Assistant'}:</b><br>
                    {message['content']}
                </div>
            """, unsafe_allow_html=True)

    # Chat input with Enter functionality
    with st.container():
        user_input = st.text_input("Message GeminiSpark...", key="user_input", 
                                   label_visibility="collapsed", on_change=send_message)
        
        col1, col2 = st.columns([6, 1])
        with col2:
            if st.button("Send"):
                send_message()

if __name__ == "__main__":
    main()
