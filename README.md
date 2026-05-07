<h1 align="center">Personal AI Agent with Local LLM & Progressive Response Rendering</h1>

<p align="center">
  <strong>A sophisticated, privacy-first personal assistant powered by local Large Language Models (LLMs).</strong><br>
  Features seamless integration with Google Workspace (Gmail, Calendar), a modern ChatGPT-like interface, and real-time progressive response streaming.
</p>

## ✨ Features

- **🧠 Local LLM Integration:** Keep your data private. All natural language processing is handled by local LLMs via a dedicated NLP Controller.
- **⚡ Progressive Response Rendering:** Enjoy a ChatGPT-like experience with token-by-token streaming responses directly to the Next.js frontend.
- **📧 Gmail Agent:** Conversational control over your inbox. Read, search, draft, and send emails without leaving the chat interface.
- **📅 Calendar Agent:** Manage your schedule intuitively. Create, search, list, and delete Google Calendar events via natural language.
- **🎨 Modern UI/UX:** A beautiful, responsive chat interface built with Next.js 16, React 19, and TailwindCSS 4, featuring Markdown rendering and dynamic UI transitions.

## 🏗️ Architecture

The project is divided into two main components:

### Backend (Python / FastAPI)
A robust RESTful API built with FastAPI that coordinates different "Agents" to execute tasks.
- **NLP Controller:** Handles prompt engineering, LLM communication, and streaming the response back to the client.
- **Master Agent:** Acts as the orchestrator, routing natural language commands to the appropriate sub-agents.
- **Gmail & Calendar Agents:** Specialized agents that interface securely with Google APIs using OAuth2 credentials.

### Frontend (Next.js / React)
A sleek, highly interactive web client.
- **Streaming UI:** Uses Server-Sent Events (SSE) or chunked HTTP responses to render text progressively.
- **Rich Text Support:** Utilizes `react-markdown` and `remark-gfm` to perfectly format code blocks, lists, and tables outputted by the LLM.

## 🛠️ Tech Stack

- **Frontend:** Next.js 16, React 19, Tailwind CSS 4, Axios
- **Backend:** Python 3, FastAPI, Pydantic, Uvicorn
- **Integrations:** Google Workspace APIs (Gmail, Calendar)

## 🚀 Getting Started

### Prerequisites
- Node.js (v18 or higher)
- Python (v3.9 or higher)
- Google Cloud Console Project with Gmail and Calendar API enabled (requires `credentials.json` and `token.pickle`)

### 1. Setup the Backend
Navigate to the `backend` directory, install the dependencies, and start the FastAPI server.
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```
*(Ensure your Google OAuth `credentials.json` is placed securely in `backend/auth/`)*

### 2. Setup the Frontend
Navigate to the `frontend` directory, install Node modules, and run the development server.
```bash
cd frontend
npm install
npm run dev
```

### 3. Usage
Open [http://localhost:3000](http://localhost:3000) in your browser. You can now start typing commands like:
- *"Draft an email to John about the project meeting tomorrow"*
- *"What meetings do I have next week?"*
- *"Cancel my 3 PM appointment on Friday"*

## 🔒 Security Note
This application requires access to highly sensitive Google APIs. Ensure that your `credentials.json`, `.env` files, and `.pickle` token files are added to your `.gitignore` and **never committed to a public repository**.
