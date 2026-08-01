"""Mattermost Bot Configuration."""

from __future__ import annotations

from pydantic import Field, SecretStr
from pydantic_settings import SettingsConfigDict
from tmmp_integrations_shared.config import BaseIntegrationConfig


class BotConfig(BaseIntegrationConfig):
    """Configuration for Mattermost WebSocket Bot Microservice."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    mattermost_url: str = Field(default="http://localhost:8065", alias="MATTERMOST_URL")
    ws_url: str = Field(default="ws://localhost:8065", alias="MATTERMOST_WS_URL")
    bot_token: SecretStr = Field(default=SecretStr("bot-token"), alias="MATTERMOST_BOT_TOKEN")
    bot_username: str = Field(default="warmupbot", alias="MATTERMOST_BOT_USERNAME")
    digest_channel_id: str = Field(default="", alias="MATTERMOST_DIGEST_CHANNEL_ID")
    host: str = Field(default="0.0.0.0", alias="BOT_SERVICE_HOST")
    port: int = Field(default=8002, alias="BOT_SERVICE_PORT")
