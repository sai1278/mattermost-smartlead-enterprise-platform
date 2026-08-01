"""Daily Digest Publisher Application Service."""

from __future__ import annotations

from tmmp_integrations_shared.logging import get_logger
from tmmp_mattermost_bot.infrastructure.mattermost_rest_adapter import MattermostBotRESTAdapter

LOGGER = get_logger(__name__)


class DailyDigestPublisher:
    """Publishes daily warmup digest reports to Mattermost channels."""

    def __init__(self, rest_adapter: MattermostBotRESTAdapter, digest_channel_id: str) -> None:
        self._rest = rest_adapter
        self._channel_id = digest_channel_id

    async def publish_digest(self, title: str, summary: str, metrics: list[dict[str, str]]) -> None:
        if not self._channel_id:
            LOGGER.warning("Digest channel ID not configured. Skipping digest.")
            return

        LOGGER.info("Publishing daily warmup digest to channel %s", self._channel_id)
        res = await self._rest.post_daily_digest(
            channel_id=self._channel_id,
            title=title,
            summary=summary,
            metrics_grid=metrics,
        )
        if res.is_fail:
            LOGGER.error("Failed to publish daily digest: %s", res.error())
