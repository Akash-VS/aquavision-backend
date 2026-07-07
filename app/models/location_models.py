"""
File: location_models.py
Purpose: Models for nearby water bodies.

Author: AquaVision AI
Project: AquaVision AI Backend
"""

from pydantic import BaseModel
from typing import List
#from pydantic import BaseModel





class NearbyWaterBody(BaseModel):

    name: str

    type: str

    latitude: float

    longitude: float

    distance_km: float

    


class NearbyWaterResponse(BaseModel):
    """
    Response containing nearby water bodies.
    """

    success: bool

    count: int

    data: list[NearbyWaterBody]

    message: str