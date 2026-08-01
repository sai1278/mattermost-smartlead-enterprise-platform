from tmmp_smartlead_sync.domain.entities import WarmupMetricsSnapshot
from tmmp_smartlead_sync.domain.events import (
    CampaignReady,
    WarmupCritical,
    WarmupWarning,
)
from tmmp_smartlead_sync.domain.policies import WarmupEvaluationPolicy


def test_policy_healthy(sample_healthy_snapshot: WarmupMetricsSnapshot):
    event = WarmupEvaluationPolicy.evaluate(sample_healthy_snapshot)
    assert isinstance(event, CampaignReady)
    assert event.inbox_rate == 98.0


def test_policy_warning():
    snap = WarmupMetricsSnapshot(
        account_id=102,
        email="warn@company.com",
        sent_count=100,
        inbox_count=90,
        spam_count=3,
        bounce_count=1,
        inbox_rate=90.0,
        spam_rate=3.0,
        bounce_rate=1.0,
    )
    event = WarmupEvaluationPolicy.evaluate(snap)
    assert isinstance(event, WarmupWarning)
    assert event.spam_rate == 3.0


def test_policy_critical():
    snap = WarmupMetricsSnapshot(
        account_id=103,
        email="crit@company.com",
        sent_count=100,
        inbox_count=80,
        spam_count=6,
        bounce_count=4,
        inbox_rate=80.0,
        spam_rate=6.0,
        bounce_rate=4.0,
    )
    event = WarmupEvaluationPolicy.evaluate(snap)
    assert isinstance(event, WarmupCritical)
    assert event.spam_rate == 6.0
    assert event.bounce_rate == 4.0
