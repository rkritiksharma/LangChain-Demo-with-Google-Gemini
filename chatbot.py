'''
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import streamlit as st  
import os
from dotenv import load_dotenv
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

# Load environment variables
load_dotenv()

LANGCHAIN_API_KEY="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"
GOOGLE_API_KEY = "AIzaSyCCw-l2HgxXQMMvDdN_CEMB2SqYwLMbuP0"
LANGCHAIN_PROJECT="default"


# Set up environment variables
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY
os.environ["LANGCHAIN_API_KEY"] = LANGCHAIN_API_KEY
os.environ["LANGCHAIN_TRACING_V2"] = "true"

# Define the prompt template
prompts = ChatPromptTemplate.from_messages(
    [
        
        ("user", "Question: {question}")
    ]
)

# Streamlit UI
st.title("LangChain Demo with Google Gemini")  
input_text = st.text_input("Search the topic you want")

# LLM setup
llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.7)
output_parser = StrOutputParser()

# Define the chain
chain = prompts | llm | output_parser  # Combining prompt, model, and parser

# Execution
if input_text:
    with st.spinner("Fetching response..."):
        response = chain.invoke({"question": input_text})  # Invoke chain with user input
        st.write("### Response:")
        st.write(response)
'''
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
    [
        ("user", "Question: {question}")
    ]
)

# Streamlit UI
st.set_page_config(page_title="LangChain Demo with Google Gemini", layout="wide")
st.title("LangChain Demo with Google Gemini")
st.write("### Ask anything and get responses powered by Google Gemini!")

# Input text area
input_text = st.text_area("Enter your question:", height=100)

# LLM setup
llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.7)
output_parser = StrOutputParser()

# Define the chain
chain = prompts | llm | output_parser  # Combining prompt, model, and parser

# Execution
if st.button("Get Response"):
    if input_text.strip():  # Check if input is not empty
        with st.spinner("Fetching response..."):
            try:
                response = chain.invoke({"question": input_text})  # Invoke chain with user input
                st.write("### Response:")
                st.write(response)
            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a question before submitting.")