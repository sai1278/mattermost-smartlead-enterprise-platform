"""Domain Entities and Core Value Objects."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum


class HealthAlertLevel(Enum):
    HEALTHY = "HEALTHY"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"
    CAMPAIGN_READY = "CAMPAIGN_READY"


@dataclass(frozen=True)
class WarmupMetricsSnapshot:
    account_id: int
    email: str
    sent_count: int
    inbox_count: int
    spam_count: int
    bounce_count: int
    inbox_rate: float
    spam_rate: float
    bounce_rate: float
    timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))
