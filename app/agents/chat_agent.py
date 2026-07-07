"""
File: chat_agent.py
Purpose: AquaVision AI Chat Agent

Author: AquaVision AI
Project: AquaVision AI Backend
"""

from app.core.logging import logger
from app.prompts.chat_prompt import CHAT_PROMPT
from app.providers.provider_manager import provider_manager


class ChatAgent:
    """
    AquaVision AI Chat Agent.
    """

    async def chat(
        self,
        message: str,
        language: str,
        ):

        logger.info("Chat Agent started.")

        prompt = CHAT_PROMPT.format(
            question=message,
            language=language,
        )

        result = await provider_manager.generate_text(
            prompt=prompt
        )

        logger.info("Chat Agent completed.")

        return {
            "provider": result["provider"],
            "answer": result["raw_response"],
            "processing_time": result["processing_time"],
        }

chat_agent = ChatAgent()