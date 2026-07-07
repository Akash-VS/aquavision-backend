"""
File: request_models.py
Purpose: Request models for AquaVision AI Backend.

Author: AquaVision AI
Project: AquaVision AI Backend
"""

from typing import Optional

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """
    AI Chat Request
    """

    question: str = Field(
        ...,
        min_length=1,
        max_length=1000,
        description="User question"
    )


class NearbyWaterRequest(BaseModel):
    """
    GPS Location Request
    """

    latitude: float = Field(
        ...,
        ge=-90,
        le=90,
        description="Latitude"
    )

    longitude: float = Field(
        ...,
        ge=-180,
        le=180,
        description="Longitude"
    )


class CompareRequest(BaseModel):
    """
    Image comparison request.
    Frontend uploads two images using multipart/form-data.
    """

    description: Optional[str] = Field(
        default=None,
        max_length=500
    )