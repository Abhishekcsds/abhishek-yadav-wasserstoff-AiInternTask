



# from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks, Request
# from fastapi.responses import JSONResponse
# from typing import List
# import shutil
# import os
# from pathlib import Path
# import fitz  # PyMuPDF

# from app.services.document_processor import process_and_store_document
# from app.services.query_handler import handle_query
# from app.services.theme_identifier import identify_themes
# from pydantic import BaseModel

# # Initialize router and ensure upload directory exists
# router = APIRouter()
# UPLOAD_DIR = Path("app/uploads")
# UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


# async def save_file_to_disk(file: UploadFile) -> str:
#     """
#     Save the incoming uploaded file to the disk under UPLOAD_DIR.
#     """
#     file_location = UPLOAD_DIR / file.filename
#     with open(file_location, "wb") as buffer:
#         shutil.copyfileobj(file.file, buffer)
#     return str(file_location)


# def extract_text_from_pdfs(filenames: List[str]) -> str:
#     """
#     Combine text content extracted from multiple PDF files.
#     """
#     combined_text = ""
#     for fname in filenames:
#         file_path = UPLOAD_DIR / fname
#         if not file_path.exists():
#             print(f"[WARNING] File not found: {file_path}")
#             continue
#         with fitz.open(file_path) as doc:
#             for page in doc:
#                 combined_text += page.get_text()
#     return combined_text.strip()


# @router.post("/upload/")
# async def upload_files(background_tasks: BackgroundTasks, files: List[UploadFile] = File(...)):
#     """
#     Endpoint to upload multiple files, save them, and start background processing.
#     """
#     try:
#         saved_file_paths = []
#         for file in files:
#             path = await save_file_to_disk(file)
#             saved_file_paths.append(path)

#         # Trigger async processing for each saved file
#         for path in saved_file_paths:
#             background_tasks.add_task(process_and_store_document, path)

#         return JSONResponse(content={"message": "Files uploaded and processing initiated."})
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"File upload error: {str(e)}")


# class QueryRequest(BaseModel):
#     query: str
#     doc_id: str = None  # Document ID is optional but usually provided by frontend


# @router.post("/query/")
# async def query_answer(request: QueryRequest):
#     """
#     Process a query against optionally a specific document.
#     """
#     try:
#         answer = await handle_query(request.query, request.doc_id)
#         return JSONResponse(content={"answer": answer})
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Query processing error: {str(e)}")


# @router.post("/themes/")
# async def get_themes_from_documents(request: Request):
#     """
#     Extract themes from selected PDF documents by combining their text and running theme identification.
#     """
#     try:
#         body = await request.json()
#         selected_files = body.get("documents", [])

#         if not selected_files:
#             raise HTTPException(status_code=400, detail="No document filenames provided.")

#         combined_text = extract_text_from_pdfs(selected_files)

#         if not combined_text:
#             raise HTTPException(status_code=404, detail="No text extracted from the selected documents.")

#         theme_result = identify_themes(combined_text)
#         themes = theme_result.get("themes", [])

#         synthesized_answer = ". ".join(themes) if themes else "No themes detected."

#         return JSONResponse(content={
#             "themes": [{"description": theme, "documents": selected_files} for theme in themes],
#             "synthesizedAnswer": synthesized_answer,
#         })
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Theme extraction failed: {str(e)}")


# @router.get("/documents/list")
# async def list_uploaded_documents():
#     """
#     Return a list of all uploaded PDF files available on the server.
#     """
#     try:
#         files = os.listdir(UPLOAD_DIR)
#         pdf_files = [f for f in files if f.lower().endswith(".pdf")]
#         file_list = [{"filename": f} for f in pdf_files]
#         return JSONResponse(content=file_list)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Could not list documents: {str(e)}")


# @router.delete("/documents/delete/{filename}")
# async def delete_uploaded_document(filename: str):
#     """
#     Remove an uploaded document file from the server storage.
#     """
#     try:
#         file_path = UPLOAD_DIR / filename
#         if file_path.exists():
#             os.remove(file_path)
#             return JSONResponse(content={"message": f"{filename} was deleted successfully."})
#         else:
#             raise HTTPException(status_code=404, detail="File not found.")
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Deletion failed: {str(e)}")




from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks, Request
from fastapi.responses import JSONResponse
from typing import List
import shutil
import os
from pathlib import Path
import fitz  # PyMuPDF
import traceback

from app.services.document_processor import process_and_store_document
from app.services.query_handler import handle_query
from app.services.theme_identifier import identify_themes
from pydantic import BaseModel

BASE_DIR = Path(__file__).resolve().parent.parent  # adjust if needed
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

router = APIRouter()

async def save_file_to_disk(file: UploadFile) -> str:
    file_location = UPLOAD_DIR / file.filename
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return str(file_location)

def extract_text_from_pdfs(filenames: List[str]) -> str:
    combined_text = ""
    for fname in filenames:
        file_path = UPLOAD_DIR / fname
        if not file_path.exists():
            print(f"[WARNING] File not found: {file_path}")
            continue
        with fitz.open(file_path) as doc:
            for page in doc:
                combined_text += page.get_text()
    return combined_text.strip()

@router.post("/upload/")
async def upload_files(background_tasks: BackgroundTasks, files: List[UploadFile] = File(...)):
    try:
        saved_file_paths = []
        for file in files:
            path = await save_file_to_disk(file)
            saved_file_paths.append(path)
        for path in saved_file_paths:
            background_tasks.add_task(process_and_store_document, path)
        return JSONResponse(content={"message": "Files uploaded and processing initiated."})
    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"File upload error: {str(e)}")

class QueryRequest(BaseModel):
    query: str
    doc_id: str = None

@router.post("/query/")
async def query_answer(request: QueryRequest):
    try:
        answer = await handle_query(request.query, request.doc_id)
        return JSONResponse(content={"answer": answer})
    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Query processing error: {str(e)}")

@router.post("/themes/")
async def get_themes_from_documents(request: Request):
    try:
        body = await request.json()
        selected_files = body.get("documents", [])
        if not selected_files:
            raise HTTPException(status_code=400, detail="No document filenames provided.")
        combined_text = extract_text_from_pdfs(selected_files)
        if not combined_text:
            raise HTTPException(status_code=404, detail="No text extracted from the selected documents.")
        theme_result = identify_themes(combined_text)
        themes = theme_result.get("themes", [])
        synthesized_answer = ". ".join(themes) if themes else "No themes detected."
        return JSONResponse(content={
            "themes": [{"description": theme, "documents": selected_files} for theme in themes],
            "synthesizedAnswer": synthesized_answer,
        })
    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Theme extraction failed: {str(e)}")

@router.get("/documents/list")
async def list_uploaded_documents():
    try:
        files = os.listdir(UPLOAD_DIR)
        pdf_files = [f for f in files if f.lower().endswith(".pdf")]
        file_list = [{"filename": f} for f in pdf_files]
        return JSONResponse(content=file_list)
    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Could not list documents: {str(e)}")

@router.delete("/documents/delete/{filename}")
async def delete_uploaded_document(filename: str):
    try:
        file_path = UPLOAD_DIR / filename
        if file_path.exists():
            os.remove(file_path)
            return JSONResponse(content={"message": f"{filename} was deleted successfully."})
        else:
            raise HTTPException(status_code=404, detail="File not found.")
    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Deletion failed: {str(e)}")
