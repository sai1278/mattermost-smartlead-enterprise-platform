"""Mattermost Bot Lifecycle Service."""

from __future__ import annotations

import asyncio
from contextlib import suppress

from tmmp_integrations_shared.logging import get_logger
from tmmp_mattermost_bot.application.event_dispatcher import BotEventDispatcher
from tmmp_mattermost_bot.infrastructure.mattermost_ws_adapter import MattermostWebSocketAdapter

LOGGER = get_logger(__name__)


class MattermostBotService:
    """Manages bot lifespan, WebSocket event listening task, and reconnect loop."""

    def __init__(
        self,
        ws_adapter: MattermostWebSocketAdapter,
        event_dispatcher: BotEventDispatcher,
    ) -> None:
        self._ws = ws_adapter
        self._dispatcher = event_dispatcher
        self._running = False
        self._task: asyncio.Task[None] | None = None

    @property
    def is_connected(self) -> bool:
        return self._running

    async def start(self) -> None:
        self._running = True
        self._task = asyncio.create_task(self._listener_loop())
        LOGGER.info("Started MattermostBotService WebSocket listener.")

    async def stop(self) -> None:
        self._running = False
        if self._task:
            self._task.cancel()
            with suppress(asyncio.CancelledError):
                await self._task
        LOGGER.info("Stopped MattermostBotService gracefully.")

    async def _listener_loop(self) -> None:
        while self._running:
            try:
                async for event in self._ws.listen_events():
                    await self._dispatcher.dispatch_ws_event(event)
            except Exception as exc:
                LOGGER.error("WebSocket listener loop error: %s. Retrying in 5s...", exc)
                await asyncio.sleep(5.0)
