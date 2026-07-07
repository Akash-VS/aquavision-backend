"""
File: config.py
Purpose: Centralized application configuration using Pydantic Settings.

Author: AquaVision AI
Project: AquaVision AI Backend
"""

from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Global application settings loaded from .env
    """

    # ==========================================================
    # Application
    # ==========================================================
    APP_NAME: str = Field(default="AquaVision AI Backend")
    APP_VERSION: str = Field(default="1.0.0")
    DEBUG: bool = Field(default=True)

    HOST: str = Field(default="0.0.0.0")
    PORT: int = Field(default=8000)

    # ==========================================================
    # Gemini
    # ==========================================================
    GEMINI_API_KEY: str = Field(default="")
    GEMINI_MODEL: str = Field(default="gemini-2.5-flash")

    # ==========================================================
    # OpenRouter
    # ==========================================================
    OPENROUTER_API_KEY: str = Field(default="")
    OPENROUTER_MODEL: str = Field(
        default="google/gemini-2.5-flash"
    )

    # ==========================================================
    # Groq
    # ==========================================================
    GROQ_API_KEY: str = Field(default="")
    GROQ_MODEL: str = Field(default="")

    # ==========================================================
    # Upload Configuration
    # ==========================================================
    UPLOAD_DIR: str = Field(default="app/uploads")
    MAX_IMAGE_SIZE_MB: int = Field(default=10)

    # ==========================================================
    # Provider Configuration
    # ==========================================================
    PROVIDER_TIMEOUT: int = Field(default=60)
    ENABLE_FALLBACK: bool = Field(default=True)

    # ==========================================================
    # News API (Future)
    # ==========================================================
    NEWS_API_KEY: str = Field(default="")
    NEWS_CACHE_DURATION: int = Field(default=7200)  # Cache duration in seconds

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """
    Returns cached application settings.
    """
    return Settings()


settings = get_settings()