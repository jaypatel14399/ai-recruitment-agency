"""Utilities for processing uploaded resume and job description files."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable, List, Dict

from .text_extractor import extract_text_from_pdf, extract_text_from_docx


SUPPORTED_EXTENSIONS = {".pdf": extract_text_from_pdf, ".docx": extract_text_from_docx}


def _extract_text(file_path: str | Path) -> str:
    """Extract plain text from a single file based on its extension.

    Parameters
    ----------
    file_path: str or Path
        The path to the file to extract text from. The file extension must be
        either ``.pdf`` or ``.docx``.

    Returns
    -------
    str
        The extracted plain text.

    Raises
    ------
    ValueError
        If the file extension is unsupported.
    """
    path = Path(file_path)
    extractor = SUPPORTED_EXTENSIONS.get(path.suffix.lower())
    if extractor is None:
        raise ValueError(f"Unsupported file type: {path.suffix}")
    return extractor(path)


def process_uploaded_files(resume_paths: List[str | Path], job_description_path: str | Path) -> Dict[str, object]:
    """Process uploaded resumes and job description into plain text.

    Parameters
    ----------
    resume_paths: list of str or Path
        Paths to resume files. Each file must be a PDF or DOCX.
    job_description_path: str or Path
        Path to the job description file (PDF or DOCX).

    Returns
    -------
    dict
        Dictionary containing the job description text under the key
        ``"job_description"`` and a list of resume dictionaries under ``"resumes"``.
    """
    resumes_output: List[Dict[str, str]] = []
    for path in resume_paths:
        text = _extract_text(path)
        resumes_output.append({"filename": Path(path).name, "text": text})

    jd_text = _extract_text(job_description_path)

    return {"job_description": jd_text, "resumes": resumes_output}
