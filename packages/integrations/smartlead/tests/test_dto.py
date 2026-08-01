from tmmp_integrations_smartlead.dto import (
    Campaign,
    EmailAccount,
    WarmupAccount,
    WarmupStats,
)
from tmmp_integrations_smartlead.models import CampaignStatus, MailboxHealth, WarmupStage


def test_warmup_account_dto():
    acc = WarmupAccount(id=101, email="user@example.com", stage=WarmupStage.RAMP_UP)
    assert acc.id == 101
    assert acc.email == "user@example.com"
    assert acc.stage == WarmupStage.RAMP_UP


def test_warmup_stats_dto():
    stats = WarmupStats(account_id=101, sent_count=50, inbox_count=48, inbox_rate=96.0)
    assert stats.account_id == 101
    assert stats.inbox_count == 48
    assert stats.inbox_rate == 96.0


def test_campaign_dto():
    c = Campaign(id=1, name="Outreach Campaign A", status=CampaignStatus.ACTIVE)
    assert c.id == 1
    assert c.status == CampaignStatus.ACTIVE


def test_email_account_dto():
    acc = EmailAccount(id=5, from_email="sales@company.com", health=MailboxHealth.EXCELLENT)
    assert acc.id == 5
    assert acc.health == MailboxHealth.EXCELLENT
