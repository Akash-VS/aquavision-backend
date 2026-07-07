"""
File: chat.py
Purpose: AquaVision AI Chat API

Author: AquaVision AI
Project: AquaVision AI Backend
"""

from fastapi import APIRouter, HTTPException

from app.agents.chat_agent import chat_agent
from app.models.chat_models import (
    ChatRequest,
    ChatResponse,
)
from app.core.logging import logger

router = APIRouter(
    prefix="/api",
    tags=["Chat"],
)


@router.post(
    "/chat",
    response_model=ChatResponse,
)
async def chat(
    request: ChatRequest,
):

    try:

        logger.info("Chat request received.")

        result = await chat_agent.chat(
            message=request.message,
            language=request.language,
        )

        return ChatResponse(
            success=True,
            provider=result["provider"],
            answer=result["answer"],
            processing_time=result["processing_time"],
        )

    except Exception as e:

        logger.exception("Chat API Error")

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )