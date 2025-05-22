# import os

# TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"  # Update if different
# UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "..", "data")
# ALLOWED_EXTENSIONS = {"pdf", "png", "jpg", "jpeg"}


import os

# Path to the Tesseract OCR executable - modify if installed elsewhere
TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Define the directory where uploaded files will be stored, relative to this file's location
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "..", "data")

# Set of permitted file extensions for uploads
ALLOWED_EXTENSIONS = {"pdf", "png", "jpg", "jpeg"}
