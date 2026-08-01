"""Mattermost Response Formatting Adapter using Mattermost SDK."""

from __future__ import annotations

from tmmp_integrations_mattermost import (
    InteractiveAttachmentBuilder,
    MarkdownBuilder,
    SlashCommandResponse,
)
from tmmp_integrations_smartlead import EmailAccount, WarmupAccount


class MattermostResponseAdapter:
    """Formats slash command output into typed Mattermost SlashCommandResponse DTOs."""

    @staticmethod
    def build_help_response() -> SlashCommandResponse:
        text = (
            MarkdownBuilder()
            .heading("Smartlead Warmup Slash Commands", level=3)
            .bullet("`/warmup status <mailbox>` - Check warmup status for a mailbox")
            .bullet("`/warmup list` - List all configured warmup mailboxes")
            .bullet("`/warmup pause <account_id>` - Pause warmup for an account")
            .bullet("`/warmup resume <account_id>` - Resume warmup for an account")
            .bullet("`/warmup help` - Show this help message")
            .build()
        )
        return SlashCommandResponse(response_type="ephemeral", text=text)

    @staticmethod
    def build_list_response(accounts: list[EmailAccount]) -> SlashCommandResponse:
        builder = MarkdownBuilder().heading("Configured Warmup Mailboxes", level=3)
        for acc in accounts:
            status_icon = "✅ Enabled" if acc.is_warmup_enabled else "⏸️ Disabled"
            item_text = (
                f"**ID {acc.id}**: `{acc.from_email}` - "
                f"{status_icon} (Limit: {acc.daily_limit}/day)"
            )
            builder.bullet(item_text)

        return SlashCommandResponse(response_type="ephemeral", text=builder.build())

    @staticmethod
    def build_status_response(account: WarmupAccount) -> SlashCommandResponse:
        attachment = (
            InteractiveAttachmentBuilder()
            .title(f"Warmup Status: {account.email}")
            .color("#0080FF" if account.warmup_status == "ACTIVE" else "#FFA500")
            .add_field("Account ID", str(account.id))
            .add_field("Warmup Status", account.warmup_status)
            .add_field("Total Sent", str(account.total_warmup_sent))
            .add_field("Total Inbox", str(account.total_warmup_landed_inbox))
            .build()
        )
        return SlashCommandResponse(
            response_type="in_channel",
            text="",
            attachments=[attachment],
        )

    @staticmethod
    def build_action_response(message: str, is_success: bool = True) -> SlashCommandResponse:
        text = f"✅ {message}" if is_success else f"❌ {message}"
        return SlashCommandResponse(response_type="ephemeral", text=text)
