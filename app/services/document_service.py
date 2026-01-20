"""
Document Service

Handles document parsing (PDF, DOCX) and resume summarization.
"""
import pdfplumber
from docx import Document
from pathlib import Path

from app.config.settings import settings
from app.services.llm_service import llm_service


class DocumentService:
    """Service for document extraction and processing."""
    
    @staticmethod
    def extract_text_from_pdf(file_path: str) -> str:
        """Extract text content from a PDF file."""
        text = []
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text.append(page_text)
        return "\n".join(text)
    
    @staticmethod
    def extract_text_from_docx(file_path: str) -> str:
        """Extract text content from a DOCX file."""
        doc = Document(file_path)
        return "\n".join(p.text for p in doc.paragraphs if p.text.strip())
    
    def extract_text(self, file_path: str) -> str:
        """
        Extract text from a document (PDF or DOCX).
        
        Args:
            file_path: Path to the document
            
        Returns:
            Extracted text content
        """
        if file_path.endswith(".pdf"):
            return self.extract_text_from_pdf(file_path)
        else:
            return self.extract_text_from_docx(file_path)
    
    def summarize_resume(self, resume_file: str) -> str:
        """
        Extract and summarize a resume file.
        
        Args:
            resume_file: Path to the resume file
            
        Returns:
            Summary of the resume
        """
        resume_text = self.extract_text(resume_file)
        return llm_service.generate_response(
            settings.SUMMARIZE_RESUME_PROMPT_PATH,
            additional_text=resume_text
        )


# Singleton instance
document_service = DocumentService()
