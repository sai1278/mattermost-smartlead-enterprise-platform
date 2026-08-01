"""Mattermost SDK Configuration."""

from __future__ import annotations

from pydantic import Field, SecretStr
from pydantic_settings import SettingsConfigDict
from tmmp_integrations_shared.config import BaseIntegrationConfig


class MattermostConfig(BaseIntegrationConfig):
    """Configuration settings for Mattermost Integration SDK."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    mattermost_url: str = Field(default="http://localhost:8065", alias="MATTERMOST_URL")
    bot_token: SecretStr = Field(default=SecretStr(""), alias="MATTERMOST_BOT_TOKEN")
    team_id: str = Field(default="", alias="MATTERMOST_TEAM_ID")
    api_version: str = Field(default="v4", alias="MATTERMOST_API_VERSION")
    timeout_seconds: float = Field(default=15.0, alias="MATTERMOST_TIMEOUT_SECONDS")
    max_retries: int = Field(default=3, alias="MATTERMOST_MAX_RETRIES")
