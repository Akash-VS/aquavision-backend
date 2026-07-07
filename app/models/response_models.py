

"""
File: response_models.py
Purpose: Response models for AquaVision AI Backend.

Author: AquaVision AI
Project: AquaVision AI Backend
"""

from typing import List

from pydantic import BaseModel

from typing import Optional

from typing import List, Optional
from pydantic import BaseModel


class WaterUseStatus(BaseModel):
    """
    Standardized status for different water uses.
    """

    status: str
    reason: str

class WaterAnalysisResponse(BaseModel):

    
    provider: Optional[str] = None

    water_type: str

    estimated_ph: float

    estimated_tds: int

    estimated_turbidity: float

    estimated_temperature: float

    pollution_score: int
    
    risk_level: Optional[str] = None

    water_quality_index: int

    confidence: int
    
    drinking: WaterUseStatus

    irrigation: WaterUseStatus

    domestic_use: WaterUseStatus

    

    recommendation: List[str]

    explanation: str


class ChatResponse(BaseModel):

    answer: str


class NearbyWaterResponse(BaseModel):

    latitude: float

    longitude: float

    nearby_water_bodies: List[str]


class ErrorResponse(BaseModel):

    success: bool = False

    message: str