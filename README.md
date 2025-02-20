
# 🚀 GeminiSpark

GeminiSpark is an AI-powered chatbot built using Streamlit, Google Gemini Pro, LangChain, FAISS, and SentenceTransformers. It provides quick, insightful responses and retains context across interactions using an efficient memory system.


## Features

- 🤖 AI-powered responses using Google Gemini Pro
- 📜 Memory retention with FAISS for contextual responses
- ⚡ Fast and optimized embeddings with SentenceTransformers
- 🌐 Built with Streamlit for an interactive UI
- 🎨 Customizable UI with enhanced CSS styling
- 📝 Downloadable chat history












## 🔧 Prerequisites

Ensure you have the following installed:

- Python 3.8+

- Streamlit

- FAISS

- LangChain

- Google Gemini API access

- SentenceTransformers


## 🔧 Installation

- Clone the repository:

```bash
git clone https://github.com/rkritiksharma/LangChain-Demo-with-Google-Gemini.git
cd LangChain-Demo-with-Google-Gemini
```

- Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

- Install dependencies:

```bash
pip install -r requirements.txt
```

- Set up environment variables: Create a .env file and add:

```bash
GOOGLE_API_KEY=your_google_api_key
LANGCHAIN_API_KEY=your_langchain_api_key
```

- Run the chatbot:
  ```bash
  streamlit run app.py
  ```  
## Usage
- Start the chatbot with streamlit run app.py

- Type your query in the input box and press Enter

- The chatbot will respond based on memory and context

- Click "Download Chat" to save your conversation


## Project Structure

```bash
LangChain-Demo-with-Google-Gemini/
│-- app.py             # Main Streamlit app
│-- requirements.txt   # Python dependencies
│-- .env.example       # Example environment variables
│-- README.md          # Project documentation
│-- assets/            # UI assets (if any)
```
## License

This project is licensed under the [MIT](https://choosealicense.com/licenses/mit/) License.


