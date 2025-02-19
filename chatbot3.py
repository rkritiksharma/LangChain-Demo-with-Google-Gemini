import os
from dotenv import load_dotenv
import streamlit as st
import time
import faiss
import numpy as np
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from sentence_transformers import SentenceTransformer

# Load environment variables
load_dotenv()

# Set up environment variables
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"

# FAISS and embedding setup
embedder = SentenceTransformer("all-MiniLM-L6-v2")
dimension = 384
index = faiss.IndexFlatL2(dimension)
memory = []
MAX_MEMORY_SIZE = 100  # Maximum number of memories to store

def store_memory(text, role="user"):
    global index, memory
    
    vector = embedder.encode([text])[0]
    
    # If we exceed max size, rebuild the index
    if len(memory) >= MAX_MEMORY_SIZE:
        # Keep the most recent 75% of memories
        keep_count = int(MAX_MEMORY_SIZE * 0.75)
        memory = memory[-keep_count:]
        
        # Rebuild index
        new_index = faiss.IndexFlatL2(dimension)
        vectors = np.array([embedder.encode([m["text"]])[0] for m in memory])
        new_index.add(vectors)
        index = new_index
    else:
        index.add(np.array([vector]))
        
    memory.append({"text": text, "role": role})

def retrieve_memory(query):
    if len(memory) == 0:
        return "No relevant past conversation found."  

    query_vector = embedder.encode([query])[0]
    distances, indices = index.search(np.array([query_vector]), k=2)

    retrieved_texts = [memory[i]["text"] for i in indices[0] if i < len(memory)]
    
    # DEBUG: Print what we retrieve
    print(f"DEBUG: Retrieved memory: {retrieved_texts}")

    return " ".join(retrieved_texts) if retrieved_texts else "No relevant past conversation found."

# Define the prompt template compatible with Gemini Pro
prompts = ChatPromptTemplate.from_messages([
    ("user", """You are GeminiSpark, a helpful assistant powered by Google Gemini. 
Respond to the user's query based on the context and recent conversation history.
Keep your responses concise, helpful, and relevant to the conversation flow.
If the user asks for jokes, provide a fresh joke each time.

Context from memory: {context}
    
Previous messages: {history}
    
Current question: {question}""")
])

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
            /* Hide the duplicate elements that Streamlit sometimes creates */
            .element-container:has(+ .element-container .stTextInput) {
                display: none;
            }
        </style>
        
        <script>
            // Add event listener for Enter key
            document.addEventListener('DOMContentLoaded', function() {
                setTimeout(function() {
                    const textInputs = document.querySelectorAll('input[type="text"]');
                    textInputs.forEach(input => {
                        input.addEventListener('keydown', function(e) {
                            if (e.key === 'Enter' && !e.shiftKey) {
                                e.preventDefault();
                                const sendButton = Array.from(document.querySelectorAll('button')).find(
                                    button => button.innerText.trim() === 'Send'
                                );
                                if (sendButton) {
                                    sendButton.click();
                                }
                            }
                        });
                    });
                }, 1000); // Delay to ensure DOM is fully loaded
            });
        </script>
    """, unsafe_allow_html=True)

def format_chat_history(messages):
    """Format the chat history into a string for the LLM context"""
    formatted = []
    for msg in messages[-6:]:  # Include only last 6 messages to keep context manageable
        formatted.append(f"{msg['role'].upper()}: {msg['content']}")
    return "\n".join(formatted)

def process_input():
    """Process the user input and generate a response"""
    # Check if there's something to process and avoid duplicate processing
    if "processing_done" in st.session_state and st.session_state.processing_done:
        st.session_state.processing_done = False
        return
        
    if st.session_state.user_input:
        user_message = st.session_state.user_input
        
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_message})
        
        # Clear input field
        current_input = user_message
        st.session_state.user_input = ""
        
        # Get context from memory
        context = retrieve_memory(current_input) or "No relevant past conversation found."
        
        # Format recent message history
        history = format_chat_history(st.session_state.messages[:-1])  # Exclude the just-added message
        
        # Generate response
        with st.spinner("Thinking..."):
            try:
                response = chain.invoke({
                    "context": context, 
                    "question": current_input,
                    "history": history
                })
                print(f"DEBUG: LLM Response -> {response}")
                
                # Store the response in session state
                st.session_state.messages.append({"role": "assistant", "content": response})
                
                # Update memory
                store_memory(current_input, role="user")
                store_memory(response, role="assistant")
                
            except Exception as e:
                error_msg = f"Sorry, I encountered an error: {str(e)}"
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
                print(f"ERROR: {e}")
                
        # Mark processing as complete for this cycle
        st.session_state.processing_done = True
        
        # Force a rerun to update the UI
        #st.rerun()

def main():
    # Set page configuration
    st.set_page_config(
        page_title="GeminiSpark",
        page_icon="💬",
        layout="wide"
    )
    
    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "user_input" not in st.session_state:
        st.session_state.user_input = ""
        
    if "processing_done" not in st.session_state:
        st.session_state.processing_done = False
    
    load_css()
    
    # Sidebar
    with st.sidebar:
        st.title("GeminiSpark")
        st.markdown("---")
        if st.button("+ New / Clear Chat"):
            st.session_state.messages = []
            # Also clear the memory index
            global index, memory
            index = faiss.IndexFlatL2(dimension)
            memory = []
            
        if st.button("Download Chat"):
            if 'messages' in st.session_state and st.session_state.messages:
                chat_history_str = "\n".join([f"{msg['role']}: {msg['content']}" for msg in st.session_state.messages])
                st.download_button(
                    label="Download Chat",
                    data=chat_history_str,
                    file_name="chat_history.txt",
                    mime="text/plain",
                )
            else:
                st.warning("No chat history to download.")
        
        st.markdown("---")
        
        # Display memory status
        st.subheader("Memory Status")
        st.text(f"Items in memory: {len(memory)}")

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
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.container():
            st.markdown(f"""
                <div class="chat-container">
                    <b>{'User' if message['role'] == 'user' else 'Assistant'}:</b><br>
                    {message['content']}
                </div>
            """, unsafe_allow_html=True)

    # Chat input with callback for handling input
    with st.container():
        st.text_input(
            "Message GeminiSpark...",
            key="user_input",
            on_change=process_input,
            label_visibility="collapsed"
        )
        
        col1, col2 = st.columns([6, 1])
        with col2:
            st.button("Send", on_click=process_input)

if __name__ == "__main__":
    main()