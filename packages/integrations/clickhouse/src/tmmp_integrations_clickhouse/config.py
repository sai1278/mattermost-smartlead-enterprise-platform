"""ClickHouse Client Configuration."""

from __future__ import annotations

from pydantic import Field, SecretStr
from pydantic_settings import SettingsConfigDict
from tmmp_integrations_shared.config import BaseIntegrationConfig


class ClickHouseConfig(BaseIntegrationConfig):
    """Configuration settings for ClickHouse columnar database client."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    url: str = Field(default="http://localhost:8123", alias="CLICKHOUSE_URL")
    database: str = Field(default="default", alias="CLICKHOUSE_DATABASE")
    user: str = Field(default="default", alias="CLICKHOUSE_USER")
    password: SecretStr = Field(default=SecretStr(""), alias="CLICKHOUSE_PASSWORD")
    timeout_seconds: float = Field(default=30.0, alias="CLICKHOUSE_TIMEOUT_SECONDS")
