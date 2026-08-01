"""Smartlead Sync Worker Configuration."""

from __future__ import annotations

from pydantic import Field, SecretStr
from pydantic_settings import SettingsConfigDict
from tmmp_integrations_shared.config import BaseIntegrationConfig


class SyncWorkerConfig(BaseIntegrationConfig):
    """Configuration for Smartlead Sync Business Microservice."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    sync_interval_seconds: int = Field(default=300, alias="SYNC_INTERVAL_SECONDS")
    webhook_secret: SecretStr = Field(default=SecretStr(""), alias="SMARTLEAD_WEBHOOK_SECRET")
    alert_channel_id: str = Field(default="", alias="MATTERMOST_ALERT_CHANNEL_ID")
    host: str = Field(default="0.0.0.0", alias="SYNC_WORKER_HOST")
    port: int = Field(default=8000, alias="SYNC_WORKER_PORT")
