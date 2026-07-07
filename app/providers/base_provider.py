"""
File: base_provider.py
Purpose: Abstract base class for all AI providers.

Author: AquaVision AI
Project: AquaVision AI Backend
"""

from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseProvider(ABC):
    """
    Abstract base class for all AI providers.

    Every provider must implement these methods.
    """

    def __init__(self, provider_name: str):
        self.provider_name = provider_name

    @abstractmethod
    async def analyze_image(
        self,
        image_path: str,
        prompt: str
    ) -> Dict[str, Any]:
        """
        Analyze an image using the provider.

        Args:
            image_path: Local image path.
            prompt: AI prompt.

        Returns:
            Dictionary containing AI response.
        """
        pass
    
    
    @abstractmethod
    async def generate_text(
        self,
        prompt: str,
    ) -> Dict[str, Any]:
        """
        Generate text response.
        Used by AquaVision Chat Assistant.
        """
        pass

    @abstractmethod
    async def health_check(self) -> bool:
        """
        Check whether the provider is available.

        Returns:
            True if provider is healthy.
        """
        pass
    
