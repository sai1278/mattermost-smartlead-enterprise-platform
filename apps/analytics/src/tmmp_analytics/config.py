"""Analytics Microservice Configuration."""

from __future__ import annotations

from pydantic import Field
from pydantic_settings import SettingsConfigDict
from tmmp_integrations_shared.config import BaseIntegrationConfig


class AnalyticsConfig(BaseIntegrationConfig):
    """Configuration for Enterprise Analytics Microservice."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    batch_size: int = Field(default=100, alias="ANALYTICS_BATCH_SIZE")
    batch_flush_seconds: float = Field(default=5.0, alias="ANALYTICS_BATCH_FLUSH_SECONDS")
    retention_days: int = Field(default=90, alias="ANALYTICS_RETENTION_DAYS")
    host: str = Field(default="0.0.0.0", alias="ANALYTICS_HOST")
    port: int = Field(default=8003, alias="ANALYTICS_PORT")
