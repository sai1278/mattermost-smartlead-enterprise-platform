"""Smartlead SDK Configuration."""

from __future__ import annotations

from pydantic import Field, SecretStr
from pydantic_settings import SettingsConfigDict
from tmmp_integrations_shared.config import BaseIntegrationConfig


class SmartleadConfig(BaseIntegrationConfig):
    """Configuration settings for Smartlead Integration SDK."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    smartlead_api_url: str = Field(
        default="https://server.smartlead.ai/api/v1", alias="SMARTLEAD_API_URL"
    )
    api_key: SecretStr = Field(default=SecretStr(""), alias="SMARTLEAD_API_KEY")
    timeout_seconds: float = Field(default=15.0, alias="SMARTLEAD_TIMEOUT_SECONDS")
    max_retries: int = Field(default=3, alias="SMARTLEAD_MAX_RETRIES")
