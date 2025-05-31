


# import os
# import uuid
# import pytesseract
# from PIL import Image
# import fitz  # PyMuPDF

# from app.services.vector_store import store_to_vector_db
# from app.core.config import settings

# # Optional: Set tesseract path on Windows
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# async def process_and_store_document(file):
#     """
#     Save uploaded file, extract text via OCR/PDF parser, and store in vector DB.
#     """
#     # Unique filename
#     unique_filename = f"{uuid.uuid4()}_{file.filename}"
#     storage_folder = "data"
#     os.makedirs(storage_folder, exist_ok=True)
#     full_path = os.path.join(storage_folder, unique_filename)

#     # Save file
#     file_bytes = await file.read()
#     with open(full_path, "wb") as out_file:
#         out_file.write(file_bytes)

#     # Determine file type
#     extension = os.path.splitext(full_path)[1].lower()
#     if extension == ".pdf":
#         extracted_text = extract_text_from_pdf(full_path)
#     elif extension in [".jpg", ".jpeg", ".png"]:
#         extracted_text = extract_text_from_image(full_path)
#     else:
#         raise ValueError(f"Unsupported file format: {extension}")

#     print(f"[DEBUG] Extracted {len(extracted_text)} chars from {unique_filename}")

#     # ✅ Await async storage
#     await store_to_vector_db(unique_filename, extracted_text)

#     return {
#         "doc_id": unique_filename,
#         "content_preview": extracted_text[:300]
#     }

# def extract_text_from_pdf(pdf_path: str) -> str:
#     """
#     Extract text from PDF using PyMuPDF.
#     """
#     text_content = ""
#     with fitz.open(pdf_path) as pdf_doc:
#         for page in pdf_doc:
#             text_content += page.get_text()
#     return text_content

# def extract_text_from_image(image_path: str) -> str:
#     """
#     OCR image using Tesseract.
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

# Optional: Windows users
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def process_and_store_document(file_path: str):
    """
    Process a document from disk (path), extract text, and store in vector DB.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    extension = os.path.splitext(file_path)[1].lower()
    filename = os.path.basename(file_path)
    if extension == ".pdf":
        extracted_text = extract_text_from_pdf(file_path)
    elif extension in [".jpg", ".jpeg", ".png"]:
        extracted_text = extract_text_from_image(file_path)
    else:
        raise ValueError(f"Unsupported file type: {extension}")

    store_to_vector_db(filename, extracted_text)

    return {
        "doc_id": filename,
        "content_preview": extracted_text[:300]
    }

def extract_text_from_pdf(pdf_path: str) -> str:
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text.strip()

def extract_text_from_image(image_path: str) -> str:
    image = Image.open(image_path)
    return pytesseract.image_to_string(image, lang=settings.OCR_LANG)
