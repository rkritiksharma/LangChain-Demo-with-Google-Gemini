#GeminiSpark: Interactive Chatbot Powered by Google Gemini
Overview
GeminiSpark is an interactive chatbot application built using Streamlit, designed to provide quick and insightful responses. It leverages Google's Gemini Pro model for natural language processing, LangChain for managing conversation flow, and FAISS for efficient memory management and context retrieval.

Features
Conversational AI: Utilizes Google Gemini Pro to generate contextually relevant and helpful responses.
Memory Management: Implements FAISS to store and retrieve conversation history, ensuring the chatbot can reference past interactions.
User-Friendly Interface: A clean and intuitive UI built with Streamlit, allowing users to easily interact with the chatbot.
Customizable: Easily adaptable for various use cases by modifying the prompt templates and memory management logic.
Feedback Mechanism: Allows users to provide feedback directly within the application.
How It Works
User Input: Users can input their queries or messages, which are processed by the chatbot.
Context Retrieval: The chatbot retrieves relevant past conversations using FAISS to maintain context.
Response Generation: Google Gemini Pro generates responses based on the current query and retrieved context.
Memory Update: Each interaction is stored in memory to enhance future responses.
Technologies Used
Streamlit: For building the interactive web interface.
Google Gemini Pro: For natural language understanding and response generation.
LangChain: For managing the conversation flow and prompt templates.
FAISS: For efficient similarity search and memory management.
SentenceTransformer: For encoding text into vectors for similarity search.
Setup and Installation
Clone the Repository:


git clone <repository-url>
cd <repository-directory>
Install Dependencies:


pip install -r requirements.txt
Run the Application:


streamlit run app.py
Environment Variables:
Ensure you have a .env file with the necessary API keys for Google Gemini and LangChain.
