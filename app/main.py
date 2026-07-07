"""
File: main.py
Purpose: AquaVision AI Backend

Author: AquaVision AI
"""

from fastapi import FastAPI

from app.core.config import settings
from app.core.logging import logger
from app.routers.analysis import router as analysis_router
from app.routers.news import router as news_router
from app.routers.location import router as location_router
from app.routers.chat import router as chat_router


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
)

app.include_router(analysis_router)
app.include_router(news_router)
app.include_router(location_router)
app.include_router(chat_router)


@app.get("/")
async def root():

    return {
        "message": "Welcome to AquaVision AI Backend",
        "version": settings.APP_VERSION,
    }


@app.get("/health")
async def health():

    return {
        "status": "healthy",
        "service": settings.APP_NAME,
    }


@app.on_event("startup")
async def startup():

    logger.info("=" * 60)
    logger.info("AquaVision AI Backend Started")
    logger.info("=" * 60)
    

