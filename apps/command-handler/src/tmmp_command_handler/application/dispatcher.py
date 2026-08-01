"""Command Dispatcher for Parsing and Routing Slash Commands."""

from __future__ import annotations

from tmmp_command_handler.application.warmup_commands import WarmupCommandHandler
from tmmp_command_handler.domain.commands import (
    WarmupHelpCommand,
    WarmupListCommand,
    WarmupPauseCommand,
    WarmupResumeCommand,
    WarmupStatusCommand,
)
from tmmp_integrations_mattermost import SlashCommandPayload, SlashCommandResponse


class CommandDispatcher:
    """Parses raw SlashCommandPayload and routes to appropriate Application Handlers."""

    def __init__(self, warmup_handler: WarmupCommandHandler) -> None:
        self._warmup_handler = warmup_handler

    async def dispatch(self, payload: SlashCommandPayload) -> SlashCommandResponse:
        parts = payload.text.strip().split()
        subcommand = parts[0].lower() if parts else "help"

        if subcommand == "status":
            mailbox = parts[1] if len(parts) > 1 else ""
            cmd = WarmupStatusCommand(
                user_id=payload.user_id,
                user_name=payload.user_name,
                channel_id=payload.channel_id,
                team_id=payload.team_id,
                mailbox=mailbox,
            )
            return await self._warmup_handler.handle_command(cmd)

        if subcommand == "list":
            cmd_list = WarmupListCommand(
                user_id=payload.user_id,
                user_name=payload.user_name,
                channel_id=payload.channel_id,
                team_id=payload.team_id,
            )
            return await self._warmup_handler.handle_command(cmd_list)

        if subcommand == "pause":
            acc_id = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 0
            cmd_pause = WarmupPauseCommand(
                user_id=payload.user_id,
                user_name=payload.user_name,
                channel_id=payload.channel_id,
                team_id=payload.team_id,
                account_id=acc_id,
            )
            return await self._warmup_handler.handle_command(cmd_pause)

        if subcommand == "resume":
            acc_id = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 0
            cmd_resume = WarmupResumeCommand(
                user_id=payload.user_id,
                user_name=payload.user_name,
                channel_id=payload.channel_id,
                team_id=payload.team_id,
                account_id=acc_id,
            )
            return await self._warmup_handler.handle_command(cmd_resume)

        cmd_help = WarmupHelpCommand(
            user_id=payload.user_id,
            user_name=payload.user_name,
            channel_id=payload.channel_id,
            team_id=payload.team_id,
        )
        return await self._warmup_handler.handle_command(cmd_help)
