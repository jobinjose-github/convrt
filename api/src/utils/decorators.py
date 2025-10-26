
from functools import wraps
import os
from typing import List

from fastapi import UploadFile
from fastapi.responses import JSONResponse


def validate_file_type(func):
    @wraps(func)
    def wrapper(self, files: List[UploadFile], source_type: str, target_type: str):
        try:
            for file in files:
                file_type = file.filename.split(".")[-1]
                if file_type != source_type:
                    return JSONResponse(
                        status_code=400,
                        content={"status": "failed", "message": f"Invalid file type: {file.filename}"}
                    )
            return func(self, files, source_type, target_type)
        except Exception as e:
            return JSONResponse(
                status_code=500,
                content={"status": "failed", "message": str(e)}
            )
    return wrapper
