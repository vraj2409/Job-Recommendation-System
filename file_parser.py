import os

from PyPDF2 import PdfReader

def read_pdf(pdf_file):
    """Read text content from a PDF file."""
    try:
        reader = PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
        return text
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

def read_txt(txt_file):
    """Read text content from a TXT file."""
    try:
        return txt_file.read().decode('utf-8')
    except Exception as e:
        return f"Error reading TXT: {str(e)}"

def read_docx(docx_file):
    """Read text content from a DOCX file."""
    try:
        from docx import Document
        doc = Document(docx_file)
        text = "\n".join([p.text for p in doc.paragraphs])
        return text
    except Exception as e:
        return f"Error reading DOCX: {str(e)}"

def parse_resume(uploaded_file):
    """Parse resume based on file type."""
    filename = uploaded_file.name.lower()
    
    if filename.endswith('.pdf'):
        return read_pdf(uploaded_file)
    elif filename.endswith('.docx'):
        return read_docx(uploaded_file)
    elif filename.endswith('.txt'):
        return read_txt(uploaded_file)
    else:
        return "Unsupported file format. Please upload PDF, DOCX, or TXT."
