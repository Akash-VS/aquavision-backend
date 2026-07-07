"""
File: master_agent.py
Purpose: Orchestrates the complete water analysis workflow.

Author: AquaVision AI
Project: AquaVision AI Backend
"""

from app.agents.analysis_agent import analysis_agent
from app.agents.recommendation_agent import recommendation_agent
from app.core.logging import logger
from app.prompts.analysis_prompt import ANALYSIS_PROMPT
from app.providers.provider_manager import provider_manager


class MasterAgent:
    """
    Main AI workflow orchestrator.
    """

    async def analyze(self, image_path: str):
        """
        Complete AI analysis workflow.

        Args:
            image_path: Temporary uploaded image path.

        Returns:
            WaterAnalysisResponse
        """

        logger.info("=" * 60)
        logger.info("AquaVision AI Analysis Started")
        logger.info("=" * 60)

        # ---------------------------------------------------
        # Step 1 : Call Provider Manager
        # ---------------------------------------------------

        provider_response = await provider_manager.analyze_image(
            image_path=image_path,
            prompt=ANALYSIS_PROMPT,
        )

        logger.info(
            f"Provider Used : {provider_response['provider']}"
        )

        # ---------------------------------------------------
        # Step 2 : Validate AI Response
        # ---------------------------------------------------

        analysis = await analysis_agent.process(
            provider_response["raw_response"]
        )

        # Preserve provider information
        analysis.provider = provider_response["provider"]

        # ---------------------------------------------------
        # Step 3 : Apply Recommendation Rules
        # ---------------------------------------------------

        analysis = await recommendation_agent.process(
            analysis
        )

        logger.info("Analysis Completed Successfully.")

        return {
    "analysis": analysis.model_dump(),
    "metadata": {
        "provider": provider_response["provider"],
        "processing_time": provider_response["processing_time"],
        "usage": provider_response.get("usage"),
    },
}


master_agent = MasterAgent()