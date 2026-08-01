"""Configuration Loader and Base Environment Settings."""

from __future__ import annotations

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseIntegrationConfig(BaseSettings):
    """Base settings model for integration configuration."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    environment: str = Field(default="development", alias="ENVIRONMENT")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    service_name: str = Field(default="integration-service", alias="SERVICE_NAME")
    enable_telemetry: bool = Field(default=True, alias="ENABLE_TELEMETRY")
