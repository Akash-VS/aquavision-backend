"""
File: analysis.py
Purpose: Water Analysis API Router

Author: AquaVision AI
Project: AquaVision AI Backend
"""

from unittest import result

from unittest import result

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.agents.master_agent import master_agent
from app.core.logging import logger
from app.services.image_service import image_service

router = APIRouter(
    prefix="/api",
    tags=["Water Analysis"],
)


@router.post("/analyze-water")
async def analyze_water(
    image: UploadFile = File(...)
):
    """
    Analyze uploaded water image.
    """

    image_path = None

    try:

        logger.info("Water analysis request received.")

        # Save uploaded image
        image_path = await image_service.save_image(image)

        # AI Analysis
        result = await master_agent.analyze(image_path)

        return  {
        "success": True,
        "data": result["analysis"],
        "metadata": result["metadata"],
        "message": "Water analysis completed successfully." }

    except Exception as e:

        logger.exception("Analysis API Error")

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    finally:

        if image_path:

            await image_service.remove_image(image_path)