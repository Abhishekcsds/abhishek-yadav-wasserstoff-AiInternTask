

# import os
# import uuid
# import pytesseract
# from PIL import Image
# import fitz  # PyMuPDF

# from app.services.vector_store import store_to_vector_db
# from app.core.config import settings

# # Set the Tesseract path for Windows (optional)
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# async def process_and_store_document(file):
#     """
#     Process uploaded file: extract text, split, embed, and store.
#     """
#     # Step 1: Save uploaded file to disk
#     filename = f"{uuid.uuid4()}_{file.filename}"
#     save_dir = "data"
#     os.makedirs(save_dir, exist_ok=True)
#     saved_path = os.path.join(save_dir, filename)

#     contents = await file.read()
#     with open(saved_path, "wb") as f:
#         f.write(contents)

#     # Step 2: Extract text based on file type
#     ext = os.path.splitext(saved_path)[1].lower()
#     if ext == ".pdf":
#         text = extract_text_from_pdf(saved_path)
#     elif ext in [".jpg", ".jpeg", ".png"]:
#         text = extract_text_from_image(saved_path)
#     else:
#         raise ValueError(f"Unsupported file type: {ext}")

#     # Step 3: Store in vector DB
#     store_to_vector_db(filename, text)

#     # Optional: clean up file
#     # os.remove(saved_path)

#     return {
#         "doc_id": filename,
#         "content_preview": text[:300]  # preview snippet
#     }

# def extract_text_from_pdf(file_path: str) -> str:
#     """Extract text from PDF using PyMuPDF"""
#     text = ""
#     doc = fitz.open(file_path)
#     for page in doc:
#         text += page.get_text()
#     return text

# def extract_text_from_image(file_path: str) -> str:
#     """Extract text from image using Tesseract OCR"""
#     image = Image.open(file_path)
#     text = pytesseract.image_to_string(image, lang=settings.OCR_LANG)
#     return text


import os
import uuid
import pytesseract
from PIL import Image
import fitz  # PyMuPDF library for PDF handling

from app.services.vector_store import store_to_vector_db
from app.core.config import settings

# Optional: Specify Tesseract OCR executable path on Windows systems
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

async def process_and_store_document(file):
    """
    Handle an uploaded document by saving it, extracting text content,
    and saving that content into the vector database.
    """
    # Generate unique filename to avoid collisions
    unique_filename = f"{uuid.uuid4()}_{file.filename}"
    storage_folder = "data"
    os.makedirs(storage_folder, exist_ok=True)  # Ensure folder exists
    full_path = os.path.join(storage_folder, unique_filename)

    # Read file bytes asynchronously and write to disk
    file_bytes = await file.read()
    with open(full_path, "wb") as out_file:
        out_file.write(file_bytes)

    # Determine file extension and extract text accordingly
    extension = os.path.splitext(full_path)[1].lower()
    if extension == ".pdf":
        extracted_text = extract_text_from_pdf(full_path)
    elif extension in [".jpg", ".jpeg", ".png"]:
        extracted_text = extract_text_from_image(full_path)
    else:
        raise ValueError(f"File format {extension} is not supported.")

    # Save the extracted text along with the filename in vector database
    store_to_vector_db(unique_filename, extracted_text)

    # Optional: Remove saved file after processing if storage is a concern
    # os.remove(full_path)

    # Return metadata including document ID and a short preview of content
    return {
        "doc_id": unique_filename,
        "content_preview": extracted_text[:300],  # Return first 300 characters as preview
    }

def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extract textual content from a PDF file using PyMuPDF.
    Concatenates text from all pages.
    """
    text_content = ""
    pdf_doc = fitz.open(pdf_path)
    for page in pdf_doc:
        text_content += page.get_text()
    return text_content

def extract_text_from_image(image_path: str) -> str:
    """
    Perform OCR on image files to retrieve text using Tesseract.
    Language is configurable via settings.
    """
    img = Image.open(image_path)
    recognized_text = pytesseract.image_to_string(img, lang=settings.OCR_LANG)
    return recognized_text
