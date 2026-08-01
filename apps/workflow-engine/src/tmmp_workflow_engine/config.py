"""Workflow Engine Configuration."""

from __future__ import annotations

from pydantic import Field
from pydantic_settings import SettingsConfigDict
from tmmp_integrations_shared.config import BaseIntegrationConfig


class WorkflowEngineConfig(BaseIntegrationConfig):
    """Configuration for Enterprise Workflow Engine Microservice."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    escalation_timeout_hours: int = Field(default=24, alias="WORKFLOW_ESCALATION_TIMEOUT_HOURS")
    readiness_inbox_threshold_pct: float = Field(
        default=95.0, alias="WORKFLOW_READINESS_THRESHOLD_PCT"
    )
    host: str = Field(default="0.0.0.0", alias="WORKFLOW_ENGINE_HOST")
    port: int = Field(default=8004, alias="WORKFLOW_ENGINE_PORT")
