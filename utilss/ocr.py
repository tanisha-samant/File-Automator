import pdfplumber
import docx
import logging
import io

logging.basicConfig(level=logging.INFO)

def extract_text_from_pdf(file):
    """Extract text from a PDF file with improved error handling."""
    try:
        # Ensure file is at the beginning
        file.seek(0)
        
        # Log file details
        logging.info(f"PDF File Size: {len(file.read())} bytes")
        file.seek(0)

        # Use context manager for safe file handling
        with pdfplumber.open(file) as pdf:
            extracted_text = ""
            for page in pdf.pages:
                page_text = page.extract_text() or ""
                extracted_text += page_text + "\n"
            
            # Trim extremely large texts
            if len(extracted_text) > 100000:
                extracted_text = extracted_text[:100000]
                logging.warning("Text truncated due to excessive length")
            
            return extracted_text.strip()
    
    except Exception as e:
        logging.error(f"PDF Text Extraction Error: {e}")
        return ""

def extract_text_from_docx(file):
    """Extract text from a DOCX file with improved error handling."""
    try:
        # Ensure file is at the beginning
        file.seek(0)
        
        # Log file details
        logging.info(f"DOCX File Size: {len(file.read())} bytes")
        file.seek(0)

        # Use docx library to extract text
        doc = docx.Document(file)
        extracted_text = "\n".join([para.text for para in doc.paragraphs])
        
        # Trim extremely large texts
        if len(extracted_text) > 100000:
            extracted_text = extracted_text[:100000]
            logging.warning("Text truncated due to excessive length")
        
        return extracted_text.strip()
    
    except Exception as e:
        logging.error(f"DOCX Text Extraction Error: {e}")
        return ""