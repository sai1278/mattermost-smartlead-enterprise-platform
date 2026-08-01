"""Smartlead SDK Data Transfer Objects."""

from __future__ import annotations

from tmmp_integrations_shared.dto import BaseDTO

from tmmp_integrations_smartlead.models import CampaignStatus, MailboxHealth, WarmupStage


class WarmupAccount(BaseDTO):
    id: int
    email: str
    warmup_status: str = "INACTIVE"
    stage: WarmupStage = WarmupStage.INITIAL
    total_warmup_sent: int = 0
    total_warmup_landed_inbox: int = 0


class WarmupStats(BaseDTO):
    account_id: int
    sent_count: int = 0
    inbox_count: int = 0
    spam_count: int = 0
    bounce_count: int = 0
    reply_count: int = 0
    inbox_rate: float = 0.0
    spam_rate: float = 0.0


class Campaign(BaseDTO):
    id: int
    name: str
    status: CampaignStatus = CampaignStatus.DRAFT
    created_at: str = ""
    account_count: int = 0


class EmailAccount(BaseDTO):
    id: int
    from_email: str
    from_name: str = ""
    daily_limit: int = 50
    is_warmup_enabled: bool = False
    health: MailboxHealth = MailboxHealth.EXCELLENT


class ReputationMetrics(BaseDTO):
    inbox_placement: float = 100.0
    spam_placement: float = 0.0
    bounce_rate: float = 0.0
    reply_rate: float = 0.0


class DailyWarmupMetrics(BaseDTO):
    date: str
    sent: int = 0
    inbox: int = 0
    spam: int = 0
