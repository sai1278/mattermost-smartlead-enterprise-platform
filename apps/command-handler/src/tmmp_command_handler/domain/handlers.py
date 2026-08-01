"""Command Handler Protocol Interface."""

from __future__ import annotations

from typing import Protocol

from tmmp_command_handler.domain.commands import Command
from tmmp_integrations_mattermost import SlashCommandResponse


class CommandHandlerProtocol(Protocol):
    """Protocol for executing typed domain commands."""

    async def handle(self, command: Command) -> SlashCommandResponse: ...
