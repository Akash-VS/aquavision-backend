"""
File: chat_models.py
Purpose: Chat request and response models.

Author: AquaVision AI
Project: AquaVision AI Backend
"""

from pydantic import BaseModel


class ChatRequest(BaseModel):
    """
    Chat request.
    """

    message: str
    
    language: str = "english"


class ChatResponse(BaseModel):
    """
    Chat response.
    """

    success: bool

    provider: str

    answer: str

    processing_time: float