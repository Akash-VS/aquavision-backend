"""
File: location_agent.py
Purpose: Handle nearby water body search.

Author: AquaVision AI
Project: AquaVision AI Backend
"""

from app.core.logging import logger
from app.models.location_models import (
    NearbyWaterBody,
    NearbyWaterResponse,
)
from app.services.location_service import location_service
#from app.services.news_service import news_service


class LocationAgent:
    """
    Agent responsible for nearby water body search.
    """

    async def process(
        self,
        latitude: float,
        longitude: float,
    ) -> NearbyWaterResponse:

        logger.info("Location Agent started.")

        water_bodies = location_service.get_nearby_water_bodies(
            latitude=latitude,
            longitude=longitude,
        )
        
#

        response = NearbyWaterResponse(
            success=True,
            count=len(water_bodies),
            data=[
                NearbyWaterBody(**item)
                for item in water_bodies
            ],
            message="Nearby water bodies found successfully."
        )

        logger.info("Location Agent completed.")

        return response


location_agent = LocationAgent()