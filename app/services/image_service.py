"""
File: image_service.py
Purpose: Image upload and temporary file management.

Author: AquaVision AI
Project: AquaVision AI Backend
"""

from pathlib import Path

import aiofiles
from fastapi import HTTPException, UploadFile

from app.core.config import settings
from app.core.logging import logger
from app.utils.file_utils import (
    delete_temp_file,
    generate_unique_filename,
    is_allowed_image,
    validate_image_size,
)


class ImageService:
    """
    Handles image upload, validation and deletion.
    """

    def __init__(self):
        self.upload_dir = Path(settings.UPLOAD_DIR)
        self.upload_dir.mkdir(parents=True, exist_ok=True)

    async def save_image(self, image: UploadFile) -> str:
        """
        Save uploaded image temporarily.

        Returns:
            Local file path.
        """

        if not is_allowed_image(image.filename):

            raise HTTPException(
                status_code=400,
                detail="Unsupported image format. Allowed: jpg, jpeg, png, webp"
            )

        filename = generate_unique_filename(image.filename)

        file_path = self.upload_dir / filename

        async with aiofiles.open(file_path, "wb") as buffer:

            content = await image.read()

            await buffer.write(content)

        if not validate_image_size(str(file_path)):

            delete_temp_file(str(file_path))

            raise HTTPException(
                status_code=400,
                detail=f"Image exceeds {settings.MAX_IMAGE_SIZE_MB} MB."
            )

        logger.info(f"Image uploaded: {filename}")

        return str(file_path)

    async def remove_image(self, file_path: str):
        """
        Delete temporary uploaded image.
        """

        delete_temp_file(file_path)

        logger.info(f"Temporary image deleted: {file_path}")


image_service = ImageService()