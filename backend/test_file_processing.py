import pytest
from pathlib import Path

from utils.file_processing import process_uploaded_files


def test_process_uploaded_files(tmp_path):
    # Use existing sample files in uploads directory
    uploads_dir = Path(__file__).resolve().parent / "uploads"
    resume_pdf = uploads_dir / "JayResumeDraft.pdf"
    resume_docx = uploads_dir / "JayResumeDraft.docx"
    jd_docx = uploads_dir / "JD.docx"

    result = process_uploaded_files([resume_pdf, resume_docx], jd_docx)

    assert "job_description" in result
    assert isinstance(result["job_description"], str)
    assert len(result["resumes"]) == 2
    assert {d["filename"] for d in result["resumes"]} == {resume_pdf.name, resume_docx.name}
    assert all("text" in d and isinstance(d["text"], str) for d in result["resumes"])  # nosec B101


def test_process_uploaded_files_unsupported(tmp_path):
    with pytest.raises(ValueError):
        process_uploaded_files(["file.txt"], "JD.docx")
