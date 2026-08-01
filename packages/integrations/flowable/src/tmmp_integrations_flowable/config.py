"""Flowable Client Configuration."""

from __future__ import annotations

from pydantic import Field, SecretStr
from pydantic_settings import SettingsConfigDict
from tmmp_integrations_shared.config import BaseIntegrationConfig


class FlowableConfig(BaseIntegrationConfig):
    """Configuration settings for Flowable BPMN Engine integration."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    url: str = Field(default="http://localhost:8080/flowable-rest", alias="FLOWABLE_URL")
    user: str = Field(default="admin", alias="FLOWABLE_USER")
    password: SecretStr = Field(default=SecretStr("test"), alias="FLOWABLE_PASSWORD")
    timeout_seconds: float = Field(default=30.0, alias="FLOWABLE_TIMEOUT_SECONDS")
