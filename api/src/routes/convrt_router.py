import base64
from typing import Annotated, List
from fastapi import APIRouter, File, Form, UploadFile, Depends
from fastapi.responses import JSONResponse

from services.file_service import FileService

router = APIRouter()


@router.post("/upload")
async def upload_file(
    files: List[UploadFile] = File(...),
    source_type: str = Form(...),
    target_type: str = Form(...),
    file_service=Depends(FileService),
):
    try:
        response = file_service.convert(files, source_type, target_type)
        return response
    except ValueError as e:
        return JSONResponse(status_code=400, content={"status": "failed", "message": str(e)})
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "failed", "message": str(e)})
