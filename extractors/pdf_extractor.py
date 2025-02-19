import pdfplumber
import pandas as pd

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file."""
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
            print(text)
    return text

def extract_tables_from_pdf(pdf_path):
    """Extracts tables from a PDF file."""
    tables = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            tables.extend(page.extract_tables())
    return tables

def save_tables_to_excel(tables, output_path):
    """Saves extracted tables to an Excel file."""
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        for i, table in enumerate(tables):
            df = pd.DataFrame(table)
            df.to_excel(writer, sheet_name=f"Table_{i+1}", index=False)