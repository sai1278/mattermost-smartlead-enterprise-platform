"""Warmup Command Handlers Application Logic."""

from __future__ import annotations

from tmmp_command_handler.domain.commands import (
    Command,
    WarmupHelpCommand,
    WarmupListCommand,
    WarmupPauseCommand,
    WarmupResumeCommand,
    WarmupStatusCommand,
)
from tmmp_command_handler.infrastructure.mattermost_adapter import MattermostResponseAdapter
from tmmp_command_handler.infrastructure.smartlead_adapter import SmartleadCommandAdapter
from tmmp_integrations_mattermost import SlashCommandResponse


class WarmupCommandHandler:
    """Application handler processing /warmup command suite."""

    def __init__(
        self,
        smartlead_adapter: SmartleadCommandAdapter,
        response_adapter: MattermostResponseAdapter,
    ) -> None:
        self._smartlead = smartlead_adapter
        self._response = response_adapter

    async def handle_command(self, command: Command) -> SlashCommandResponse:
        if isinstance(command, WarmupHelpCommand):
            return self._response.build_help_response()

        if isinstance(command, WarmupListCommand):
            res_list = await self._smartlead.get_accounts()
            if res_list.is_ok:
                return self._response.build_list_response(res_list.unwrap())
            return self._response.build_action_response(
                f"Failed to fetch accounts: {res_list.error()}", is_success=False
            )

        if isinstance(command, WarmupStatusCommand):
            if not command.mailbox:
                return self._response.build_action_response(
                    "Please specify a mailbox or account ID.", is_success=False
                )
            try:
                acc_id = int(command.mailbox)
                res_status = await self._smartlead.get_warmup_status(acc_id)
                if res_status.is_ok:
                    return self._response.build_status_response(res_status.unwrap())
                return self._response.build_action_response(
                    f"Account {acc_id} not found", is_success=False
                )
            except ValueError:
                return self._response.build_action_response(
                    "Invalid account ID specified.", is_success=False
                )

        if isinstance(command, WarmupPauseCommand):
            res_pause = await self._smartlead.pause_warmup(command.account_id)
            if res_pause.is_ok:
                return self._response.build_action_response(
                    f"Paused warmup for account {command.account_id}"
                )
            return self._response.build_action_response(
                f"Failed to pause warmup: {res_pause.error()}", is_success=False
            )

        if isinstance(command, WarmupResumeCommand):
            res_resume = await self._smartlead.resume_warmup(command.account_id)
            if res_resume.is_ok:
                return self._response.build_action_response(
                    f"Resumed warmup for account {command.account_id}"
                )
            return self._response.build_action_response(
                f"Failed to resume warmup: {res_resume.error()}", is_success=False
            )

        return self._response.build_help_response()
