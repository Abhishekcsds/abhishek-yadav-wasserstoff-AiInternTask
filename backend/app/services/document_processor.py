

# import os
# import uuid
# import pytesseract
# from PIL import Image
# import fitz  # PyMuPDF library for PDF handling

# from app.services.vector_store import store_to_vector_db
# from app.core.config import settings

# # Optional: Specify Tesseract OCR executable path on Windows systems
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# async def process_and_store_document(file):
#     """
#     Handle an uploaded document by saving it, extracting text content,
#     and saving that content into the vector database.
#     """
#     # Generate unique filename to avoid collisions
#     unique_filename = f"{uuid.uuid4()}_{file.filename}"
#     storage_folder = "data"
#     os.makedirs(storage_folder, exist_ok=True)  # Ensure folder exists
#     full_path = os.path.join(storage_folder, unique_filename)

#     # Read file bytes asynchronously and write to disk
#     file_bytes = await file.read()
#     with open(full_path, "wb") as out_file:
#         out_file.write(file_bytes)

#     # Determine file extension and extract text accordingly
#     extension = os.path.splitext(full_path)[1].lower()
#     if extension == ".pdf":
#         extracted_text = extract_text_from_pdf(full_path)
#     elif extension in [".jpg", ".jpeg", ".png"]:
#         extracted_text = extract_text_from_image(full_path)
#     else:
#         raise ValueError(f"File format {extension} is not supported.")

#     # Save the extracted text along with the filename in vector database
#     store_to_vector_db(unique_filename, extracted_text)

#     # Optional: Remove saved file after processing if storage is a concern
#     # os.remove(full_path)

#     # Return metadata including document ID and a short preview of content
#     return {
#         "doc_id": unique_filename,
#         "content_preview": extracted_text[:300],  # Return first 300 characters as preview
#     }

# def extract_text_from_pdf(pdf_path: str) -> str:
#     """
#     Extract textual content from a PDF file using PyMuPDF.
#     Concatenates text from all pages.
#     """
#     text_content = ""
#     pdf_doc = fitz.open(pdf_path)
#     for page in pdf_doc:
#         text_content += page.get_text()
#     return text_content

# def extract_text_from_image(image_path: str) -> str:
#     """
#     Perform OCR on image files to retrieve text using Tesseract.
#     Language is configurable via settings.
#     """
#     img = Image.open(image_path)
#     recognized_text = pytesseract.image_to_string(img, lang=settings.OCR_LANG)
#     return recognized_text



import os
import uuid
import pytesseract
from PIL import Image
import fitz  # PyMuPDF

from app.services.vector_store import store_to_vector_db
from app.core.config import settings

# Optional: Set tesseract path on Windows
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

async def process_and_store_document(file):
    """
    Save uploaded file, extract text via OCR/PDF parser, and store in vector DB.
    """
    # Unique filename
    unique_filename = f"{uuid.uuid4()}_{file.filename}"
    storage_folder = "data"
    os.makedirs(storage_folder, exist_ok=True)
    full_path = os.path.join(storage_folder, unique_filename)

    # Save file
    file_bytes = await file.read()
    with open(full_path, "wb") as out_file:
        out_file.write(file_bytes)

    # Determine file type
    extension = os.path.splitext(full_path)[1].lower()
    if extension == ".pdf":
        extracted_text = extract_text_from_pdf(full_path)
    elif extension in [".jpg", ".jpeg", ".png"]:
        extracted_text = extract_text_from_image(full_path)
    else:
        raise ValueError(f"Unsupported file format: {extension}")

    print(f"[DEBUG] Extracted {len(extracted_text)} chars from {unique_filename}")

    # ✅ Await async storage
    await store_to_vector_db(unique_filename, extracted_text)

    return {
        "doc_id": unique_filename,
        "content_preview": extracted_text[:300]
    }

def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extract text from PDF using PyMuPDF.
    """
    text_content = ""
    with fitz.open(pdf_path) as pdf_doc:
        for page in pdf_doc:
            text_content += page.get_text()
    return text_content

def extract_text_from_image(image_path: str) -> str:
    """
    OCR image using Tesseract.
    """
    img = Image.open(image_path)
    recognized_text = pytesseract.image_to_string(img, lang=settings.OCR_LANG)
    return recognized_text
