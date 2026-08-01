from datetime import datetime

from tmmp_analytics.domain.models import DailyMetrics, WarmupMetrics


def test_warmup_metrics_dataclass():
    now = datetime.utcnow()
    m = WarmupMetrics(
        mailbox="test@domain.com",
        timestamp=now,
        total_sent=100,
        total_inbox=95,
        total_spam=5,
        total_replies=12,
    )
    assert m.mailbox == "test@domain.com"
    assert m.total_sent == 100
    assert m.total_inbox == 95


def test_daily_metrics_dataclass():
    d = DailyMetrics(
        date_str="2026-08-01",
        total_sent=1000,
        total_inbox=980,
        total_spam=20,
        inbox_rate_pct=98.0,
    )
    assert d.date_str == "2026-08-01"
    assert d.inbox_rate_pct == 98.0
