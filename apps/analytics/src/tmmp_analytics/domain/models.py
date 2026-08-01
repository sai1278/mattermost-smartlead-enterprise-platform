"""Domain Models for Analytics Service."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class WarmupMetrics:
    mailbox: str
    timestamp: datetime
    total_sent: int
    total_inbox: int
    total_spam: int
    total_replies: int


@dataclass(frozen=True)
class DailyMetrics:
    date_str: str
    total_sent: int
    total_inbox: int
    total_spam: int
    inbox_rate_pct: float


@dataclass(frozen=True)
class MailboxTrend:
    domain: str
    period_days: int
    avg_deliverability_pct: float
    total_volume: int


@dataclass(frozen=True)
class AlertHistory:
    alert_id: str
    timestamp: datetime
    account_email: str
    severity: str
    message: str


@dataclass(frozen=True)
class HealthSnapshot:
    status: str
    database_connected: bool
    buffered_events_count: int
