"""
File: analysis_agent.py
Purpose: Validate and process AI water analysis response.

Author: AquaVision AI
Project: AquaVision AI Backend
"""

import json

from pydantic import ValidationError

from app.core.logging import logger
from app.models.response_models import WaterAnalysisResponse


class AnalysisAgent:
    """
    Converts raw AI JSON response into
    a validated WaterAnalysisResponse object.
    """

    async def process(self, raw_response: str) -> WaterAnalysisResponse:
        """
        Process AI response.

        Args:
            raw_response: JSON string returned by AI.

        Returns:
            WaterAnalysisResponse
        """

        logger.info("Analysis Agent started.")

        try:

            cleaned_response = raw_response.strip()

            if cleaned_response.startswith("```json"):
                cleaned_response = cleaned_response.replace("```json", "")

            if cleaned_response.endswith("```"):
                cleaned_response = cleaned_response.replace("```", "")

            cleaned_response = cleaned_response.strip()

            response_dict = json.loads(cleaned_response)

            result = WaterAnalysisResponse(**response_dict)

            logger.info("Analysis completed successfully.")

            return result

        except ValidationError as e:

            logger.error("Response validation failed.")

            raise RuntimeError(
                f"Pydantic Validation Error: {e}"
            )

        except json.JSONDecodeError:

            logger.error("Invalid JSON returned by provider.")

            raise RuntimeError(
                "Provider returned invalid JSON."
            )

        except Exception as e:

            logger.exception("Analysis Agent Error")

            raise RuntimeError(str(e))


analysis_agent = AnalysisAgent()