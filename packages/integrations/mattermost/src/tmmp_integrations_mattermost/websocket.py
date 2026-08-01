"""Mattermost WebSocket Client for Async Event Streaming."""

from __future__ import annotations

import json
from collections.abc import AsyncGenerator
from typing import Any

import websockets
from tmmp_integrations_shared.errors import IntegrationError
from tmmp_integrations_shared.logging import get_logger

LOGGER = get_logger(__name__)


class MattermostWebSocketEvent:
    """Parsed Mattermost WebSocket Event Payload."""

    def __init__(self, event_data: dict[str, Any]) -> None:
        self.event: str = event_data.get("event", "")
        self.data: dict[str, Any] = event_data.get("data", {})
        self.broadcast: dict[str, Any] = event_data.get("broadcast", {})
        self.seq: int = event_data.get("seq", 0)


class MattermostWebSocketClient:
    """Async WebSocket client for listening to real-time Mattermost events."""

    def __init__(self, ws_url: str, bot_token: str) -> None:
        self.ws_url = ws_url.rstrip("/") + "/api/v4/websocket"
        self.bot_token = bot_token
        self._connected = False

    async def connect_and_listen(self) -> AsyncGenerator[MattermostWebSocketEvent, None]:
        """Connect to WebSocket stream, authenticate, and yield incoming events."""
        headers = {"Authorization": f"Bearer {self.bot_token}"}
        try:
            async with websockets.connect(self.ws_url, extra_headers=headers) as ws:
                self._connected = True
                LOGGER.info("Connected to Mattermost WebSocket at %s", self.ws_url)

                # Send authentication challenge
                auth_payload = {
                    "seq": 1,
                    "action": "authentication_challenge",
                    "data": {"token": self.bot_token},
                }
                await ws.send(json.dumps(auth_payload))

                async for message in ws:
                    try:
                        raw_data = json.loads(message)
                        event = MattermostWebSocketEvent(raw_data)
                        yield event
                    except json.JSONDecodeError:
                        LOGGER.warning("Received non-JSON WebSocket frame: %s", message)

        except Exception as exc:
            self._connected = False
            LOGGER.error("WebSocket connection failure: %s", exc)
            raise IntegrationError(f"WebSocket failure: {exc}") from exc
