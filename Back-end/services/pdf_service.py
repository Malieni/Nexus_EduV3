from PyPDF2 import PdfReader
from typing import Optional
import io


async def extract_text_from_pdf(pdf_file: bytes) -> str:
    """Extrai texto de um arquivo PDF"""
    try:
        pdf_file_obj = io.BytesIO(pdf_file)
        pdf_reader = PdfReader(pdf_file_obj)
        
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        
        return text.strip()
    
    except Exception as e:
        raise Exception(f"Erro ao extrair texto do PDF: {str(e)}")

