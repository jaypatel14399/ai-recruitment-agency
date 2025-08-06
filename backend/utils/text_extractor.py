"""Utility functions for extracting text from document formats."""

from __future__ import annotations

from pathlib import Path

import fitz  # PyMuPDF
from docx import Document


def extract_text_from_pdf(file_path: str | Path) -> str:
    """Extract text from a PDF file.

    Parameters
    ----------
    file_path: str or Path
        Path to the PDF file.

    Returns
    -------
    str
        Extracted plain text.

    Raises
    ------
    RuntimeError
        If the file cannot be read or parsed.
    """
    try:
        path = Path(file_path)
        text_parts = []
        with fitz.open(path) as doc:
            for page in doc:
                text_parts.append(page.get_text())
        return "".join(text_parts)
    except Exception as exc:  # pragma: no cover - basic exception handling
        raise RuntimeError(f"Failed to extract text from PDF '{file_path}': {exc}") from exc


def extract_text_from_docx(file_path: str | Path) -> str:
    """Extract text from a DOCX file.

    Parameters
    ----------
    file_path: str or Path
        Path to the DOCX file.

    Returns
    -------
    str
        Extracted plain text.

    Raises
    ------
    RuntimeError
        If the file cannot be read or parsed.
    """
    try:
        doc = Document(str(file_path))
        return "\n".join(paragraph.text for paragraph in doc.paragraphs)
    except Exception as exc:  # pragma: no cover - basic exception handling
        raise RuntimeError(f"Failed to extract text from DOCX '{file_path}': {exc}") from exc