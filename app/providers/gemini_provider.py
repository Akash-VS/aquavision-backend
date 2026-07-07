"""
File: gemini_provider.py
Purpose: Gemini Vision Provider

Author: AquaVision AI
Project: AquaVision AI Backend
"""

from typing import Any, Dict

from google import genai
from google.genai import types

from app.core.config import settings
from app.core.logging import logger
from app.providers.base_provider import BaseProvider
from app.utils.file_utils import detect_mime_type


class GeminiProvider(BaseProvider):
    """
    Gemini Vision Provider
    """

    def __init__(self):
        super().__init__("Gemini")

        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY
        )

        self.model = settings.GEMINI_MODEL

    async def analyze_image(
        self,
        image_path: str,
        prompt: str,
    ) -> Dict[str, Any]:
        """
        Analyze image using Gemini Vision.
        """

        logger.info("Gemini analysis started.")

        try:

            with open(image_path, "rb") as image_file:

                image_bytes = image_file.read()

            response = self.client.models.generate_content(
                model=self.model,
                contents=[
                    prompt,
                    types.Part.from_bytes(
                        data=image_bytes,
                        mime_type=detect_mime_type(image_path)
                    
                    ),
                ],
            )

            logger.info("Gemini analysis completed.")

            return {
                "success": True,
                "provider": self.provider_name,
                "raw_response": response.text,
            }

        except Exception as e:

            logger.exception("Gemini Provider Error")

            raise RuntimeError(str(e))
        
        
    async def generate_text(
        self,
        prompt: str,
    ) -> Dict[str, Any]:
        """
        Generate text using Gemini.
        """

        logger.info("Gemini text generation started.")

        try:

            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
            )

            logger.info("Gemini text generation completed.")

            return {
                "success": True,
                "provider": self.provider_name,
                "raw_response": response.text,
            }

        except Exception as e:

            logger.exception("Gemini Text Generation Error")

            raise RuntimeError(str(e))

    async def health_check(self) -> bool:
        """
        Simple provider health check.
        """

        try:

            self.client.models.list()

            return True

        except Exception:

            return False