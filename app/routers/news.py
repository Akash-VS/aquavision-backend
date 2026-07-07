"""
File: news.py
Purpose: News API endpoints.

Author: AquaVision AI
Project: AquaVision AI Backend
"""

from fastapi import APIRouter, HTTPException

from app.core.logging import logger
from app.services.news_service import news_service

router = APIRouter(
    prefix="/api",
    tags=["News"],
)


@router.get("/news")
async def get_news():
    """
    Get latest environmental news.
    """

    try:

        logger.info("News request received.")

        articles = news_service.fetch_news()

        return {
            "success": True,
            "count": len(articles),
            "data": articles,
            "message": "Latest news fetched successfully."
        }

    except Exception as e:

        logger.exception("News API Error")

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )