import pytesseract
from PIL import Image
import pdfplumber

def extract_text_from_scanned_pdf(pdf_path):
    """Extracts text from a scanned PDF using OCR."""
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            # Convert each page to an image
            image = page.to_image(resolution=300).original
            text += pytesseract.image_to_string(image)
    return text