"""Bot Event Handler Protocol Interface."""

from __future__ import annotations

from typing import Protocol

from tmmp_mattermost_bot.domain.events import BotEvent


class BotEventHandlerProtocol(Protocol):
    """Protocol for processing bot domain events."""

    async def handle_event(self, event: BotEvent) -> None: ...
