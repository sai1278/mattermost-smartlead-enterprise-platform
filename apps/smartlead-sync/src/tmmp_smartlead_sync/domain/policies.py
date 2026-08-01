"""Domain Policy Rules for Warmup Evaluation."""

from __future__ import annotations

from tmmp_smartlead_sync.domain.entities import WarmupMetricsSnapshot
from tmmp_smartlead_sync.domain.events import (
    CampaignReady,
    WarmupCritical,
    WarmupEvent,
    WarmupHealthy,
    WarmupWarning,
)


class WarmupEvaluationPolicy:
    """Business Policy evaluating mailbox metrics and producing Domain Events."""

    CRITICAL_SPAM_THRESHOLD: float = 5.0
    WARNING_SPAM_THRESHOLD: float = 2.0
    CRITICAL_BOUNCE_THRESHOLD: float = 3.0
    CAMPAIGN_READY_INBOX_THRESHOLD: float = 95.0

    @classmethod
    def evaluate(cls, snapshot: WarmupMetricsSnapshot) -> WarmupEvent:
        """Evaluate snapshot metrics against threshold rules."""
        if (
            snapshot.spam_rate >= cls.CRITICAL_SPAM_THRESHOLD
            or snapshot.bounce_rate >= cls.CRITICAL_BOUNCE_THRESHOLD
        ):
            reason = (
                f"Critical metrics detected! Spam rate: {snapshot.spam_rate:.1f}%, "
                f"Bounce rate: {snapshot.bounce_rate:.1f}%"
            )
            return WarmupCritical(
                account_id=snapshot.account_id,
                email=snapshot.email,
                reason=reason,
                spam_rate=snapshot.spam_rate,
                bounce_rate=snapshot.bounce_rate,
            )

        if snapshot.spam_rate >= cls.WARNING_SPAM_THRESHOLD:
            reason = f"Elevated spam rate detected: {snapshot.spam_rate:.1f}%"
            return WarmupWarning(
                account_id=snapshot.account_id,
                email=snapshot.email,
                reason=reason,
                spam_rate=snapshot.spam_rate,
            )

        if snapshot.inbox_rate >= cls.CAMPAIGN_READY_INBOX_THRESHOLD and snapshot.sent_count >= 50:
            return CampaignReady(
                account_id=snapshot.account_id,
                email=snapshot.email,
                inbox_rate=snapshot.inbox_rate,
            )

        return WarmupHealthy(
            account_id=snapshot.account_id,
            email=snapshot.email,
            snapshot=snapshot,
        )
