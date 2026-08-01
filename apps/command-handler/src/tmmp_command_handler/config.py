"""Mattermost Command Handler Configuration."""

from __future__ import annotations

from pydantic import Field, SecretStr
from pydantic_settings import SettingsConfigDict
from tmmp_integrations_shared.config import BaseIntegrationConfig


class CommandHandlerConfig(BaseIntegrationConfig):
    """Configuration for Mattermost Command Handler Microservice."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    mattermost_token: SecretStr = Field(
        default=SecretStr("mattermost-verification-token"),
        alias="MATTERMOST_VERIFICATION_TOKEN",
    )
    host: str = Field(default="0.0.0.0", alias="COMMAND_HANDLER_HOST")
    port: int = Field(default=8001, alias="COMMAND_HANDLER_PORT")
