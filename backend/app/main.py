


# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from app.api.routes import router as api_router

# # Initialize FastAPI application with a descriptive title
# app = FastAPI(title="Document Research Chatbot with Groq LLM")

# # Configure Cross-Origin Resource Sharing (CORS) settings
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:3000"],  # Allow requests from this origin
#     allow_credentials=True,                    # Support cookies and authentication headers
#     allow_methods=["*"],                       # Permit all HTTP methods (GET, POST, etc.)
#     allow_headers=["*"],                       # Accept all headers in requests
# )

# # Register API routes, all prefixed with '/api'
# app.include_router(api_router, prefix="/api")


# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.staticfiles import StaticFiles
# from fastapi.responses import FileResponse
# from pathlib import Path

# from app.api.routes import router as api_router

# # Initialize FastAPI app
# app = FastAPI(title="Document Research Chatbot with Groq LLM")

# # CORS configuration for frontend (update allowed origin in production)
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:3000"],  # Or "*" in dev, or your frontend domain
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Include API routes under /api
# app.include_router(api_router, prefix="/api")

# # ----- Serve React Frontend -----
# build_dir = Path(__file__).resolve().parent / "build"

# # Serve static files (CSS, JS, images)
# if build_dir.exists():
#     app.mount("/static", StaticFiles(directory=build_dir / "static"), name="static")

#     # Root URL serves index.html
#     @app.get("/")
#     async def serve_root():
#         return FileResponse(build_dir / "index.html")

#     # Fallback route for React Router (SPA)
#     @app.get("/{full_path:path}")
#     async def serve_spa(full_path: str):
#         target_file = build_dir / full_path
#         if target_file.exists() and target_file.is_file():
#             return FileResponse(target_file)
#         return FileResponse(build_dir / "index.html")


# app/main.py
# backend/app/main.py

# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.staticfiles import StaticFiles
# from fastapi.responses import FileResponse
# from pathlib import Path
# import os

# from app.api.routes import router as api_router

# app = FastAPI(title="Document Research Chatbot with Groq LLM")

# # CORS settings
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:3000"],  # frontend dev server
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Include backend API routes
# app.include_router(api_router, prefix="/api")

# # ----- Serve React Frontend -----
# build_dir = Path(__file__).resolve().parent.parent / "build"

# if build_dir.exists():
#     app.mount("/static", StaticFiles(directory=build_dir / "static"), name="static")

#     @app.get("/")
#     async def serve_root():
#         return FileResponse(build_dir / "index.html")

#     @app.get("/{full_path:path}")
#     async def serve_spa(full_path: str):
#         target_file = build_dir / full_path
#         if target_file.exists() and target_file.is_file():
#             return FileResponse(target_file)
#         return FileResponse(build_dir / "index.html")

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, Response
from pathlib import Path
import os

from app.api.routes import router as api_router

app = FastAPI(title="Document Research Chatbot with Groq LLM")

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Change or extend origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include backend API routes under /api
app.include_router(api_router, prefix="/api")

# Path to React build folder (backend/build)
build_dir = Path(__file__).resolve().parent.parent / "build"

if build_dir.exists() and (build_dir / "index.html").exists():
    # Mount static files (JS, CSS, images, etc.) served from /static
    app.mount("/static", StaticFiles(directory=build_dir / "static"), name="static")

    @app.get("/", include_in_schema=False)
    async def serve_root():
        return FileResponse(build_dir / "index.html")

    @app.get("/{full_path:path}", include_in_schema=False)
    async def serve_spa(full_path: str):
        target_file = build_dir / full_path
        if target_file.exists() and target_file.is_file():
            return FileResponse(target_file)
        return FileResponse(build_dir / "index.html")
else:
    # If build directory is missing, return a simple message on root
    @app.get("/", include_in_schema=False)
    async def missing_build():
        return Response(
            content="Frontend build files not found. Please build your React app and copy it to the backend/build folder.",
            media_type="text/plain",
            status_code=500,
        )
