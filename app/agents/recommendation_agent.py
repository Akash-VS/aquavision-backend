"""
File: recommendation_agent.py
Purpose: Generate water safety recommendations based on analysis.

Author: AquaVision AI
Project: AquaVision AI Backend
"""

from typing import List

from app.core.logging import logger
from app.models.response_models import WaterAnalysisResponse


def get_risk_level(score: int) -> str:
    """
    Determine risk level based on pollution score.
    """

    if score <= 20:
        return "Excellent"
    elif score <= 40:
        return "Good"
    elif score <= 60:
        return "Moderate"
    elif score <= 80:
        return "Poor"
    else:
        return "Critical"


class RecommendationAgent:
    """
    Rule-based recommendation engine.
    """

    async def process(
        self,
        analysis: WaterAnalysisResponse,
    ) -> WaterAnalysisResponse:
        """
        Apply recommendation rules.
        """

        logger.info("Recommendation Agent started.")

        # =====================================================
        # Risk Level
        # =====================================================

        analysis.risk_level = get_risk_level(
            analysis.pollution_score
        )

        recommendations: List[str] = []

        # =====================================================
        # Drinking Water Rules
        # =====================================================

        if analysis.pollution_score >= 80:

            analysis.drinking.status = "Not Safe"
            analysis.drinking.reason = (
                "Very high pollution score indicates severe contamination."
            )

            recommendations.extend([
                "Do not consume directly.",
                "Use RO + UV purification.",
                "Laboratory testing is recommended."
            ])

        elif analysis.pollution_score >= 50:

            analysis.drinking.status = "Treatment Required"
            analysis.drinking.reason = (
                "Moderate pollution detected. Treatment is recommended before drinking."
            )

            recommendations.extend([
                "Boiling is recommended.",
                "Use a domestic water purifier."
            ])

        else:

            analysis.drinking.status = "Likely Safe"
            analysis.drinking.reason = (
                "Low estimated pollution score."
            )

            recommendations.append(
                "Suitable for general domestic use after basic filtration."
            )

        # =====================================================
        # Irrigation Rules
        # =====================================================

        if analysis.pollution_score >= 80:

            analysis.irrigation.status = "Not Recommended"
            analysis.irrigation.reason = (
                "Severely polluted water may damage crops and soil."
            )

        elif analysis.pollution_score >= 50:

            analysis.irrigation.status = "Limited Use"
            analysis.irrigation.reason = (
                "Use only after appropriate treatment."
            )

        else:

            analysis.irrigation.status = "Suitable"
            analysis.irrigation.reason = (
                "Estimated quality appears acceptable for irrigation."
            )

        # =====================================================
        # Domestic Use Rules
        # =====================================================

        if analysis.pollution_score >= 70:

            analysis.domestic_use.status = "Not Recommended"
            analysis.domestic_use.reason = (
                "Unsafe for household use without proper treatment."
            )

        else:

            analysis.domestic_use.status = "Suitable After Treatment"
            analysis.domestic_use.reason = (
                "Basic treatment is recommended before household use."
            )

        # =====================================================
        # TDS Rules
        # =====================================================

        if analysis.estimated_tds > 500:

            recommendations.append(
                "High TDS detected. Reverse Osmosis (RO) is recommended."
            )

        # =====================================================
        # Turbidity Rules
        # =====================================================

        if analysis.estimated_turbidity > 50:

            recommendations.append(
                "High turbidity detected. Sediment filtration is recommended."
            )

        # =====================================================
        # pH Rules
        # =====================================================

        if analysis.estimated_ph < 6.5:

            recommendations.append(
                "Water appears acidic."
            )

        elif analysis.estimated_ph > 8.5:

            recommendations.append(
                "Water appears alkaline."
            )

        # =====================================================
        # Water Type Rules
        # =====================================================

        water_type = analysis.water_type.lower()

        if "drain" in water_type:

            recommendations.append(
                "Drainage water is not suitable for drinking."
            )

        if "sea" in water_type:

            recommendations.append(
                "Sea water requires desalination before drinking."
            )

        if "pond" in water_type:

            recommendations.append(
                "Pond water should always be purified before use."
            )

        if "lake" in water_type:

            recommendations.append(
                "Lake water should be filtered and disinfected before use."
            )

        if "river" in water_type:

            recommendations.append(
                "River water should be purified before drinking."
            )

        # =====================================================
        # Remove Duplicate Recommendations
        # =====================================================

        analysis.recommendation = list(dict.fromkeys(recommendations))

        logger.info("Recommendation Agent completed.")

        return analysis


recommendation_agent = RecommendationAgent()