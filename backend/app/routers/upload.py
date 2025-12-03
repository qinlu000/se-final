import uuid
from pathlib import Path

from fastapi import APIRouter, File, UploadFile

from app.schemas import UploadResponse

router = APIRouter(tags=["upload"])

BASE_DIR = Path(__file__).resolve().parent.parent.parent
UPLOAD_DIR = BASE_DIR / "static" / "uploads"


@router.post("/upload", response_model=UploadResponse)
async def upload_file(file: UploadFile = File(...)) -> UploadResponse:
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    extension = Path(file.filename).suffix if file.filename else ""
    unique_name = f"{uuid.uuid4().hex}{extension}"
    destination = UPLOAD_DIR / unique_name

    content = await file.read()
    destination.write_bytes(content)

    url = f"/static/uploads/{unique_name}"
    return UploadResponse(url=url)
