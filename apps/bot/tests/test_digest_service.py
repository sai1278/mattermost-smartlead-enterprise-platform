import asyncio
from unittest.mock import AsyncMock, MagicMock

from tmmp_integrations_shared.dto import Result
from tmmp_mattermost_bot.application.digest_service import DailyDigestPublisher


def test_daily_digest_publisher():
    rest_adapter = MagicMock()
    rest_adapter.post_daily_digest = AsyncMock(return_value=Result.ok(MagicMock()))

    publisher = DailyDigestPublisher(rest_adapter, digest_channel_id="chan-digest-99")

    metrics = [
        {"title": "Active Mailboxes", "value": "42"},
        {"title": "Overall Deliverability", "value": "98.5%"},
    ]

    async def _test():
        await publisher.publish_digest("Daily Summary", "Warmup operational status", metrics)
        assert rest_adapter.post_daily_digest.called

    asyncio.run(_test())
