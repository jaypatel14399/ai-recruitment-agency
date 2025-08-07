from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
import shutil
from pathlib import Path
from typing import List

from utils.file_processing import process_uploaded_files
from utils.ranking import rank_resumes_by_similarity

app = FastAPI()

# Allow React frontend to call FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Adjust if frontend runs elsewhere
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@app.post("/upload-resumes")
async def upload_resumes(
    resumes: List[UploadFile] = File(...),
    job_description: UploadFile = File(...)
):
    resume_paths = []
    
    # Save resumes
    for resume in resumes:
        file_path = UPLOAD_DIR / resume.filename
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(resume.file, buffer)
        resume_paths.append(str(file_path))
    
    # Save job description
    jd_path = UPLOAD_DIR / job_description.filename
    with open(jd_path, "wb") as buffer:
        shutil.copyfileobj(job_description.file, buffer)

    processed = process_uploaded_files(resume_paths, jd_path)
    ranked = rank_resumes_by_similarity(
        processed["resumes"], processed["job_description"]
    )
    top_matches = [
        {"filename": r.get("filename"), "score": r.get("score")}
        for r in ranked
    ]

    return {
        "message": "Files uploaded successfully",
        "resumes": resume_paths,
        "job_description": str(jd_path),
        "top_matches": top_matches,
    }
