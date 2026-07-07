"""
File: research_service.py
Purpose: Search latest information about nearby water bodies.

Author: AquaVision AI
Project: AquaVision AI Backend
"""

import requests

from app.core.logging import logger
from app.core.config import settings


class ResearchService:

    SEARCH_URL = "https://api.currentsapi.services/v1/search"

    def search(self, water_body: str):

        logger.info(
            f"Searching latest reports for: {water_body}"
        )

        params = {
            "apiKey": settings.NEWS_API_KEY,
            "keywords": water_body,
            "language": "en",
            "page_size": 5,
        }

        response = requests.get(
            self.SEARCH_URL,
            params=params,
            timeout=20,
        )

        response.raise_for_status()

        data = response.json()

        results = []

        for article in data.get("news", []):

            results.append(
                {
                    "title": article.get("title"),
                    "description": article.get("description"),
                    "url": article.get("url"),
                    "published": article.get("published"),
                }
            )

        logger.info(
            f"{len(results)} reports found."
        )

        return results


research_service = ResearchService()