"""
resume_parser.py
Extracts raw text from an uploaded resume file (PDF or DOCX).
"""

import os
from pypdf import PdfReader
import docx


def extract_text_from_pdf(file_path_or_buffer):
    """Extract text from every page of a PDF file."""
    reader = PdfReader(file_path_or_buffer)
    text_parts = []
    for page in reader.pages:
        page_text = page.extract_text() or ""
        text_parts.append(page_text)
    return "\n".join(text_parts)


def extract_text_from_docx(file_path_or_buffer):
    """Extract text from every paragraph of a DOCX file."""
    document = docx.Document(file_path_or_buffer)
    text_parts = [para.text for para in document.paragraphs]
    return "\n".join(text_parts)


def extract_resume_text(file_path_or_buffer, filename):
    """
    Detects file type from filename extension and routes to the
    correct extractor. Works with both a file path (str) and a
    file-like buffer (e.g. from Streamlit's file_uploader).
    """
    ext = os.path.splitext(filename)[1].lower()

    if ext == ".pdf":
        return extract_text_from_pdf(file_path_or_buffer)
    elif ext == ".docx":
        return extract_text_from_docx(file_path_or_buffer)
    else:
        raise ValueError(f"Unsupported file type: {ext}. Please upload a PDF or DOCX file.")


if __name__ == "__main__":
    # Quick manual test:
    # python resume_parser.py sample_resumes/sample1.pdf
    import sys
    if len(sys.argv) > 1:
        path = sys.argv[1]
        print(extract_resume_text(path, path))
    else:
        print("Usage: python resume_parser.py <path_to_resume>")