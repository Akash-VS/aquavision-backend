"""
File: file_utils.py
Purpose: File handling utilities.

Author: AquaVision AI
Project: AquaVision AI Backend
"""

import mimetypes
import os
import uuid
from pathlib import Path

from app.core.config import settings


ALLOWED_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
}


def generate_unique_filename(filename: str) -> str:
    """
    Generate a unique filename while preserving extension.
    """

    extension = Path(filename).suffix.lower()

    return f"{uuid.uuid4().hex}{extension}"


def get_file_extension(filename: str) -> str:
    """
    Return file extension.
    """

    return Path(filename).suffix.lower()


def is_allowed_image(filename: str) -> bool:
    """
    Validate supported image formats.
    """

    return get_file_extension(filename) in ALLOWED_EXTENSIONS


def detect_mime_type(file_path: str) -> str:
    """
    Detect MIME type from file.
    """

    mime_type, _ = mimetypes.guess_type(file_path)

    return mime_type or "application/octet-stream"


def validate_image_size(file_path: str) -> bool:
    """
    Check image size against configured limit.
    """

    size_mb = os.path.getsize(file_path) / (1024 * 1024)

    return size_mb <= settings.MAX_IMAGE_SIZE_MB


def delete_temp_file(file_path: str):
    """
    Delete temporary uploaded image.
    """

    try:

        if os.path.exists(file_path):
            os.remove(file_path)

    except Exception:
        pass