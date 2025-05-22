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

## 🧱 Recommended Folder Structure

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
├── frontend/ # React UI without Tailwind
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

### 📌 Backend
- **FastAPI** – lightweight API framework
- **Pytesseract** – OCR for scanned files
- **LangChain** – prompt chaining and memory handling
- **Groq API** – high-performance LLM responses
- **ChromaDB** – document vector indexing
- **PyMuPDF** – PDF text extraction
- **SQLAlchemy** – for optional persistent data models

### 🖥️ Frontend
- **React.js** – modern JavaScript frontend
- **CSS Modules / Vanilla CSS** – for component styling
- **Axios** – for API calls
- **React Router** – for navigation

---

## 🔧 Setup Instructions

### 🐍 Backend

1. **Navigate to the backend directory**:
   ```bash
   cd chatbot_theme_identifier/backend


1. Create a virtual environment and install dependencies:

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

2. Run the server:
uvicorn app.main:app --reload

3. Ensure you have Tesseract installed and added to PATH.

4. Environment Variables (Optional .env):

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