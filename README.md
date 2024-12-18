# CodeSage

**CodeSage** is an AI-powered code review tool that uses advanced language models (Mistral, Llama, GPT-3.5) to analyze and review codebases, providing actionable feedback and suggestions for improvement. The project features a React-based frontend and a Python FastAPI backend for seamless user interaction and API handling.

## Project Structure

CodeSage/ ├── .idea/ # IDE configuration files (specific to IntelliJ IDEA) ├── .vscode/ # VS Code workspace settings ├── Backend/ # Backend Python FastAPI codebase ├── Frontend/ # Frontend React codebase ├── README.md # Project documentation

yaml
Copy code

---

## **1. Backend**

The `Backend` directory contains the Python FastAPI server responsible for handling API requests, invoking AI models, and managing backend services.

- **Tech Stack**: Python, FastAPI, OpenAI/Mistral/Llama models, Docker (optional for deployment)

### **Setup**
1. **Install dependencies**:
   Navigate to the `Backend` directory and set up a virtual environment:
   ```bash
   cd Backend
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
Run the backend server: Start the FastAPI development server:

bash
Copy code
uvicorn main:app --reload
By default, the server runs at http://127.0.0.1:8000.

Environment Variables: Set up the following environment variables in a .env file:

makefile
Copy code
OPENAI_API_KEY=<your_openai_api_key>
MISTRAL_API_KEY=<your_mistral_api_key>
LLAMA_API_KEY=<your_llama_api_key>
Endpoints:

/review-code: Accepts code snippets and returns reviews using the selected AI model.
/health: Simple health-check endpoint.