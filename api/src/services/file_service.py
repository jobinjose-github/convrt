from abc import ABC, abstractmethod
from typing import List
from fastapi import UploadFile
from fastapi.responses import StreamingResponse
from io import BytesIO
from zipfile import ZipFile

from utils.decorators import validate_file_type
from services.image_service import ImageService
from services.service import Service
from utils.utils import Utility


class FileService(Service):
    def __init__(self):
        self.utility = Utility()
        self.imageService = ImageService()

    def zip_files(self, responses: List[dict], files: List[UploadFile], target_type: str) -> StreamingResponse:
        """Create an in-memory zip from multiple converted files"""
        zip_buffer = BytesIO()

        with ZipFile(zip_buffer, "w") as zip_archive:
            for file, response in zip(files, responses):
                # Read converted file bytes
                converted_bytes = response["output"].read()

                # Construct the filename for the zip
                original_name = file.filename.rsplit(".", 1)[0]
                zip_filename = f"{original_name}.{target_type.lower()}"

                # Add to zip
                zip_archive.writestr(zip_filename, converted_bytes)

        zip_buffer.seek(0)
        return StreamingResponse(
            zip_buffer,
            media_type="application/zip",
            headers={"Content-Disposition": 'attachment; filename="converted_files.zip"'}
        )

    @validate_file_type
    def convert(self, files: List[UploadFile], source_type: str, target_type: str) -> StreamingResponse:
        """Convert single or multiple files"""
        if not files:
            raise ValueError("No files provided")

        service_type = self.utility.get_service_type(source_type)
        service_obj = getattr(self, service_type)

        if len(files) == 1:
            # Single file conversion
            response = service_obj.convert(files[0], source_type, target_type)
            return StreamingResponse(
                response["output"],
                media_type=response["media_type"],
                headers=response["headers"]
            )

        responses = []
        for file in files:
            response = service_obj.convert(file, source_type, target_type)
            responses.append(response)

        # Return a zip of all converted files
        return self.zip_files(responses, files, target_type)
