


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router as api_router

# Initialize FastAPI application with a descriptive title
app = FastAPI(title="Document Research Chatbot with Groq LLM")

# Configure Cross-Origin Resource Sharing (CORS) settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow requests from this origin
    allow_credentials=True,                    # Support cookies and authentication headers
    allow_methods=["*"],                       # Permit all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],                       # Accept all headers in requests
)

# Register API routes, all prefixed with '/api'
app.include_router(api_router, prefix="/api")
