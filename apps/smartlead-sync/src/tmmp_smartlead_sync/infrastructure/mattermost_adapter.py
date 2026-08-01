"""Mattermost Alert Adapter wrapping SDK Client."""

from __future__ import annotations

from tmmp_integrations_mattermost import (
    InteractiveAttachmentBuilder,
    MarkdownBuilder,
    MattermostClient,
)
from tmmp_integrations_shared.dto import Result
from tmmp_integrations_shared.errors import IntegrationError
from tmmp_smartlead_sync.domain.events import (
    CampaignReady,
    WarmupCritical,
    WarmupEvent,
    WarmupWarning,
)


class MattermostAlertAdapter:
    """Adapter posting domain event notifications to Mattermost."""

    def __init__(self, client: MattermostClient, channel_id: str) -> None:
        self._client = client
        self._channel_id = channel_id

    async def dispatch_event_notification(
        self, event: WarmupEvent
    ) -> Result[None, IntegrationError]:
        if not self._channel_id:
            return Result.ok(None)

        if isinstance(event, WarmupCritical):
            title = "🔴 CRITICAL: Mailbox Warmup Issue"
            color = "#FF0000"
            body = (
                MarkdownBuilder()
                .bold("Mailbox:")
                .text(event.email)
                .newline()
                .bold("Reason:")
                .text(event.reason)
                .build()
            )
        elif isinstance(event, WarmupWarning):
            title = "⚠️ WARNING: Elevated Spam Rate"
            color = "#FFA500"
            body = (
                MarkdownBuilder()
                .bold("Mailbox:")
                .text(event.email)
                .newline()
                .bold("Spam Rate:")
                .text(f"{event.spam_rate:.1f}%")
                .build()
            )
        elif isinstance(event, CampaignReady):
            title = "🚀 CAMPAIGN READY: Warmup Target Reached"
            color = "#00FF00"
            body = (
                MarkdownBuilder()
                .bold("Mailbox:")
                .text(event.email)
                .newline()
                .bold("Inbox Placement:")
                .text(f"{event.inbox_rate:.1f}%")
                .build()
            )
        else:
            return Result.ok(None)

        attachment = (
            InteractiveAttachmentBuilder()
            .title(title)
            .text(body)
            .color(color)
            .add_field("Account ID", str(event.account_id))
            .build()
        )

        res = await self._client.create_post(
            channel_id=self._channel_id,
            message="",
            props={"attachments": [attachment]},
        )
        if res.is_ok:
            return Result.ok(None)
        return Result.fail(res.error() or IntegrationError("Mattermost post failed"))
