"""
File: provider_manager.py
Purpose: Manage AI providers and automatic fallback.

Author: AquaVision AI
Project: AquaVision AI Backend
"""

import time
from typing import Any, Dict, List

from app.core.config import settings
from app.core.logging import logger

from app.providers.base_provider import BaseProvider
from app.providers.gemini_provider import GeminiProvider
from app.providers.openrouter_provider import OpenRouterProvider
from app.providers.groq_provider import GroqProvider


class ProviderManager:
    """
    Handles automatic provider fallback.

    Order:
        1. Gemini
        2. OpenRouter
        3. Groq
    """

    def __init__(self):

        self.providers: List[BaseProvider] = []

        if settings.GEMINI_API_KEY:
            self.providers.append(GeminiProvider())

        if settings.OPENROUTER_API_KEY:
            self.providers.append(OpenRouterProvider())

        if settings.GROQ_API_KEY:
            self.providers.append(GroqProvider())

        logger.info(
            f"Provider Manager initialized with {len(self.providers)} provider(s)."
        )

    # ============================================================
    # Image Analysis
    # ============================================================

    async def analyze_image(
        self,
        image_path: str,
        prompt: str,
    ) -> Dict[str, Any]:

        return await self._execute(
            method="analyze_image",
            image_path=image_path,
            prompt=prompt,
        )

    # ============================================================
    # Text Generation
    # ============================================================

    async def generate_text(
        self,
        prompt: str,
    ) -> Dict[str, Any]:

        return await self._execute(
            method="generate_text",
            prompt=prompt,
        )

    # ============================================================
    # Common Fallback Logic
    # ============================================================

    async def _execute(
        self,
        method: str,
        **kwargs,
    ) -> Dict[str, Any]:

        if not self.providers:
            raise RuntimeError("No AI providers configured.")

        errors = []

        for provider in self.providers:

            logger.info("=" * 60)
            logger.info(f"Trying Provider : {provider.provider_name}")

            start_time = time.perf_counter()

            try:

                response = await getattr(provider, method)(**kwargs)

                elapsed = round(
                    time.perf_counter() - start_time,
                    2,
                )

                logger.info(
                    f"{provider.provider_name} succeeded "
                    f"({elapsed} sec)"
                )

                return {
                    "success": True,
                    "provider": provider.provider_name,
                    "processing_time": elapsed,
                    "raw_response": response["raw_response"],
                    "usage": response.get("usage"),
                }

            except Exception as exc:

                elapsed = round(
                    time.perf_counter() - start_time,
                    2,
                )

                logger.warning(
                    f"{provider.provider_name} failed "
                    f"after {elapsed} sec"
                )

                logger.error(str(exc))

                errors.append(
                    {
                        "provider": provider.provider_name,
                        "processing_time": elapsed,
                        "error": str(exc),
                    }
                )

        logger.error("=" * 60)
        logger.error("All AI Providers Failed")
        logger.error("=" * 60)

        raise RuntimeError(
            {
                "message": "All AI providers failed.",
                "errors": errors,
            }
        )


provider_manager = ProviderManager()