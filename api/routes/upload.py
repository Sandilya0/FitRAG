from fastapi import APIRouter, UploadFile, File, HTTPException
import shutil
import os
from src.utils.config import RAW_PAPERS_DIR
from src.user_data.whoop_parser import parse_whoop_csv

router = APIRouter()

WHOOP_UPLOAD_PATH = "data/raw/whoop/latest_whoop.csv"


@router.post("/upload/whoop")
async def upload_whoop(file: UploadFile = File(...)):
    """Upload WHOOP CSV export."""
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="File must be a CSV")

    os.makedirs("data/raw/whoop", exist_ok=True)

    with open(WHOOP_UPLOAD_PATH, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        profile = parse_whoop_csv(WHOOP_UPLOAD_PATH)
        return {
            "message": "WHOOP data uploaded successfully",
            "profile": profile
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/upload/pdf")
async def upload_pdf(file: UploadFile = File(...)):
    """Upload a new research paper PDF."""
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="File must be a PDF")

    save_path = os.path.join(RAW_PAPERS_DIR, file.filename)

    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "message": f"PDF uploaded successfully: {file.filename}",
        "path": save_path
    }