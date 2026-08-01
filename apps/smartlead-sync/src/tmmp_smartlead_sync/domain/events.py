"""Domain Events for Warmup Evaluation."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from tmmp_smartlead_sync.domain.entities import WarmupMetricsSnapshot


@dataclass(frozen=True)
class WarmupEvent:
    account_id: int
    email: str
    timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))


@dataclass(frozen=True)
class WarmupHealthy(WarmupEvent):
    snapshot: WarmupMetricsSnapshot | None = None


@dataclass(frozen=True)
class WarmupWarning(WarmupEvent):
    reason: str = ""
    spam_rate: float = 0.0


@dataclass(frozen=True)
class WarmupCritical(WarmupEvent):
    reason: str = ""
    spam_rate: float = 0.0
    bounce_rate: float = 0.0


@dataclass(frozen=True)
class CampaignReady(WarmupEvent):
    inbox_rate: float = 0.0
