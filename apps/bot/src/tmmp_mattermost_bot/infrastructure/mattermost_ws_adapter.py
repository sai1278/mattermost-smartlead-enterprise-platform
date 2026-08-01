"""Mattermost WebSocket Adapter for Real-Time Event Listening."""

from __future__ import annotations

from collections.abc import AsyncGenerator

from tmmp_integrations_mattermost import MattermostWebSocketClient, MattermostWebSocketEvent
from tmmp_integrations_shared.logging import get_logger

LOGGER = get_logger(__name__)


class MattermostWebSocketAdapter:
    """Adapter wrapping Mattermost SDK WebSocket client."""

    def __init__(self, ws_url: str, bot_token: str) -> None:
        self._client = MattermostWebSocketClient(ws_url=ws_url, bot_token=bot_token)

    async def listen_events(self) -> AsyncGenerator[MattermostWebSocketEvent, None]:
        LOGGER.info("Starting WebSocket event listener loop...")
        async for event in self._client.connect_and_listen():
            yield event
