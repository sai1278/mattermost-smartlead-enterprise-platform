"""Response Builder Application Service."""

from __future__ import annotations

from tmmp_command_handler.infrastructure.mattermost_adapter import MattermostResponseAdapter
from tmmp_integrations_mattermost import SlashCommandResponse


class CommandResponseBuilder:
    """Facade for MattermostResponseAdapter."""

    def __init__(self) -> None:
        self._adapter = MattermostResponseAdapter()

    def help_response(self) -> SlashCommandResponse:
        return self._adapter.build_help_response()
