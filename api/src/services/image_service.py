from fastapi import UploadFile
from PIL import Image
import io
import os
from services.service import Service

class ImageService(Service):
    def __init__(self):
        pass

    def png_jpg(self, file: UploadFile):
        try:
            file_bytes= file.file.read()
            image = Image.open(io.BytesIO(file_bytes))
            if image.mode in ("RGBA", "P"):
                image = image.convert("RGB")
            output_buffer = io.BytesIO()
            image.save(output_buffer, format="JPEG")
            output_buffer.seek(0)
            return {
                "output": output_buffer,
                "media_type": "image/jpeg",
                "headers": {"Content-Disposition": f"attachment; filename={os.path.splitext(file.filename)[0]}.jpg"}
            }
        except Exception as e:
            raise e
    
    def convert(self, file: UploadFile, source_type: str, target_type: str):
        return getattr(self, f"{source_type}_{target_type}")(file)
