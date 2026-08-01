"""Smartlead Domain Enums and Core Value Objects."""

from __future__ import annotations

from enum import Enum


class WarmupStage(Enum):
    INITIAL = "INITIAL"
    RAMP_UP = "RAMP_UP"
    MAINTENANCE = "MAINTENANCE"
    PAUSED = "PAUSED"


class CampaignStatus(Enum):
    DRAFT = "DRAFT"
    ACTIVE = "ACTIVE"
    PAUSED = "PAUSED"
    COMPLETED = "COMPLETED"


class MailboxHealth(Enum):
    EXCELLENT = "EXCELLENT"
    GOOD = "GOOD"
    POOR = "POOR"
    CRITICAL = "CRITICAL"


class WebhookEventType(Enum):
    EMAIL_SENT = "EMAIL_SENT"
    EMAIL_OPENED = "EMAIL_OPENED"
    EMAIL_REPLIED = "EMAIL_REPLIED"
    EMAIL_BOUNCED = "EMAIL_BOUNCED"
    WARMUP_PAUSED = "WARMUP_PAUSED"
