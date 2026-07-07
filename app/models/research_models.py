"""
File: research_models.py
Purpose: Research models for latest water reports.

Author: AquaVision AI
Project: AquaVision AI Backend
"""

from pydantic import BaseModel


class LatestReport(BaseModel):
    """
    Latest information about a water body.
    """

    summary: str

    risk_level: str

    latest_findings: list[str]

    source_count: int


class ResearchResponse(BaseModel):
    """
    AI research response.
    """

    water_body: str

    report: LatestReport