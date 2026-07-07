"""
File: location.py
Purpose: Nearby water bodies API.

Author: AquaVision AI
Project: AquaVision AI Backend
"""

from fastapi import APIRouter, HTTPException

from app.agents.location_agent import location_agent
from app.core.logging import logger

router = APIRouter(
    prefix="/api",
    tags=["Location"],
)


@router.get("/nearby-water")
async def nearby_water(
    lat: float,
    lon: float,
):
    """
    Find nearby water bodies using GPS coordinates.
    """

    try:

        logger.info("Nearby Water API called.")

        result = await location_agent.process(
            latitude=lat,
            longitude=lon,
        )

        return result

    except Exception as e:

        logger.exception("Nearby Water API Error")

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )