"""
Document Service

Handles document parsing (PDF, DOCX) and resume summarization.
"""
import logging
from pathlib import Path

import pdfplumber
from docx import Document

from app.config.settings import settings
from app.services.llm_service import llm_service

logger = logging.getLogger(__name__)

SUPPORTED_EXTENSIONS = {".pdf", ".docx"}


class DocumentService:
    """Service for document extraction and processing."""

    @staticmethod
    def extract_text_from_pdf(file_path: str) -> str:
        """Extract text content from a PDF file."""
        text_parts = []
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)
        return "\n".join(text_parts)

    @staticmethod
    def extract_text_from_docx(file_path: str) -> str:
        """Extract text content from a DOCX file."""
        doc = Document(file_path)
        return "\n".join(p.text for p in doc.paragraphs if p.text.strip())

    def extract_text(self, file_path: str) -> str:
        """Extract text from a document based on its file extension.

        Args:
            file_path: Path to the document

        Returns:
            Extracted text content

        Raises:
            ValueError: If the file extension is not supported
        """
        ext = Path(file_path).suffix.lower()

        if ext == ".pdf":
            return self.extract_text_from_pdf(file_path)
        elif ext == ".docx":
            return self.extract_text_from_docx(file_path)
        else:
            raise ValueError(
                f"Format non supporté: '{ext}'. "
                f"Formats acceptés: {', '.join(SUPPORTED_EXTENSIONS)}"
            )

    def summarize_resume(self, resume_file: str) -> str:
        """Extract and summarize a resume file.

        Args:
            resume_file: Path to the resume file

        Returns:
            Summary of the resume, or empty string on failure
        """
        try:
            resume_text = self.extract_text(resume_file)
            if not resume_text.strip():
                logger.warning("Extracted resume text is empty: %s", resume_file)
                return ""

            return llm_service.generate_response(
                settings.SUMMARIZE_RESUME_PROMPT_PATH,
                additional_text=resume_text,
            )
        except (ValueError, OSError) as e:
            logger.error("Failed to process resume '%s': %s", resume_file, e)
            return ""


document_service = DocumentService()
