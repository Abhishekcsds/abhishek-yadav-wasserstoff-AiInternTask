# 📚 Chatbot Theme Identifier

**Chatbot Theme Identifier** is an intelligent document analysis platform designed to help users upload, process, and explore scanned or digital documents. It extracts textual data using OCR, identifies recurring themes across multiple files, and allows users to query content via a conversational chatbot that returns cited responses.

---

## 🧩 Overview

This system blends document OCR, natural language processing, and a responsive frontend to create an end-to-end solution for document research. It's useful in academic research, compliance audits, and legal document review where understanding cross-document themes is essential.

---

## ⚙️ Core Features

- 📤 Upload PDFs and image-based documents  
- 🧠 Extract text with OCR (Pytesseract)  
- 🧵 Detect recurring themes across multiple documents  
- 💬 Chatbot interface for question-answering with citation links  
- 📄 View and manage uploaded files  
- 📑 Group topics and generate summarized insights  

---

## 🧱 Folder Structure

chatbot_theme_identifier/
├── backend/
│ ├── app/
│ │ ├── api/ # Routes and endpoints
│ │ ├── core/ # Logic handlers (OCR, NLP, LLM)
│ │ ├── models/ # Pydantic models and schemas
│ │ ├── services/ # Text processing and vector DB logic
│ │ ├── main.py # FastAPI entry point
│ │ └── config.py # Environment and settings
│ ├── data/ # Sample or uploaded document storage
│ ├── Dockerfile
│ └── requirements.txt
├── frontend/ # React UI
│ ├── public/
│ └── src/
│ ├── components/ # UploadForm, DocumentList, ChatInterface, ThemeDisplay
│ └── pages/ # Home and routing setup
├── docs/ # Documentation and architecture guides
├── tests/ # Backend unit and integration tests
├── demo/ # Screenshots, sample documents, demo video
└── README.md


---

## 🚀 Technologies Used

### Backend
- **FastAPI** – Lightweight API framework  
- **Pytesseract** – OCR for scanned files  
- **LangChain** – Prompt chaining and memory handling  
- **Groq API** – High-performance LLM responses  
- **ChromaDB** – Document vector indexing  
- **PyMuPDF** – PDF text extraction  
- **SQLAlchemy** – For optional persistent data models  

### Frontend
- **React.js** – Modern JavaScript frontend  
- **CSS Modules / Vanilla CSS** – Component styling  
- **Axios** – API calls  
- **React Router** – Navigation  

---

## 🔧 Setup Instructions

### 🐍 Backend

1. Navigate to backend:

   ```bash
   cd chatbot_theme_identifier/backend


python -m venv venv
venv\Scripts\activate    # On Windows
pip install -r requirements.txt

uvicorn app.main:app --reload

Make sure Tesseract OCR is installed and available in your PATH.

GROQ_API_KEY=your_groq_key
OPENAI_API_KEY=your_openai_key


🌐 Frontend
Navigate to frontend:


cd ../frontend
Install dependencies:


npm install
Start the dev server:


npm start
Visit http://localhost:3000

📦 CRA Info (React Users Only)
This frontend was bootstrapped with Create React App.

Available Scripts
npm start – Runs the app in development mode

npm test – Launches the test runner

npm run build – Builds the app for production

npm run eject – Copies build config for advanced customization

See the CRA documentation for more.

📘 Learn More
React Docs

Create React App Docs

FastAPI Docs

LangChain Docs

Groq