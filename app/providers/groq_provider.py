"""
File: groq_provider.py
Purpose: Groq Vision Provider

Author: AquaVision AI
Project: AquaVision AI Backend
"""

import base64
from typing import Any, Dict

from openai import AsyncOpenAI

from app.core.config import settings
from app.core.logging import logger
from app.providers.base_provider import BaseProvider
from app.utils.file_utils import detect_mime_type


class GroqProvider(BaseProvider):
    """
    Groq Provider.
    """

    def __init__(self):
        super().__init__("Groq")

        self.client = AsyncOpenAI(
            api_key=settings.GROQ_API_KEY,
            base_url="https://api.groq.com/openai/v1",
        )

        self.model = settings.GROQ_MODEL

    async def analyze_image(
        self,
        image_path: str,
        prompt: str,
    ) -> Dict[str, Any]:

        logger.info("Groq analysis started.")

        try:

            with open(image_path, "rb") as image_file:
                image_bytes = image_file.read()

            image_base64 = base64.b64encode(image_bytes).decode("utf-8")

            mime_type = detect_mime_type(image_path)

            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": prompt,
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:{mime_type};base64,{image_base64}"
                                },
                            },
                        ],
                    }
                ],
                max_tokens=1500,
                temperature=0.2,
            )

            logger.info("Groq analysis completed.")

            return {
                "success": True,
                "provider": self.provider_name,
                "raw_response": response.choices[0].message.content,
                "usage": response.usage.model_dump()
                if response.usage
                else None,
            }

        except Exception as e:

            logger.exception("Groq Provider Error")

            raise RuntimeError(str(e))
        
        
    async def generate_text(
        self,
        prompt: str,
    ) -> Dict[str, Any]:
        """
        Generate text using Groq.
        """

        logger.info("Groq text generation started.")

        try:

            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                max_tokens=1000,
                temperature=0.3,
            )

            logger.info("Groq text generation completed.")

            return {
                "success": True,
                "provider": self.provider_name,
                "raw_response": response.choices[0].message.content,
                "usage": response.usage.model_dump()
                if response.usage
                else None,
            }

        except Exception as e:

            logger.exception("Groq Text Generation Error")

            raise RuntimeError(str(e))

    async def health_check(self) -> bool:

        try:

            await self.client.models.list()
            return True

        except Exception:
            return False