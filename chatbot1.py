import os
from dotenv import load_dotenv
import streamlit as st
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

# Streamlit UI
st.set_page_config(page_title="LangChain Demo with Google Gemini", layout="wide")
st.title("LangChain Demo with Google Gemini")
st.write("### Ask anything and get responses powered by Google Gemini!")

# Initialize chat history in session state if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Enter your question here"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.spinner("Fetching response..."):
        try:
            response = chain.invoke({"question": prompt})
            # Display assistant response in chat message container
            with st.chat_message("assistant"):
                st.markdown(response)
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"An error occurred: {e}")