"""Mattermost REST Adapter wrapping SDK client for Bot Actions."""

from __future__ import annotations

from typing import Any

from tmmp_integrations_mattermost import (
    InteractiveAttachmentBuilder,
    MarkdownBuilder,
    MattermostClient,
    PostDTO,
)
from tmmp_integrations_shared.dto import Result
from tmmp_integrations_shared.errors import IntegrationError


class MattermostBotRESTAdapter:
    """Adapter facilitating bot REST actions (posting, replying, digest publishing)."""

    def __init__(self, client: MattermostClient) -> None:
        self._client = client

    async def post_message(
        self,
        channel_id: str,
        message: str,
        root_id: str = "",
        props: dict[str, Any] | None = None,
    ) -> Result[PostDTO, IntegrationError]:
        return await self._client.create_post(
            channel_id=channel_id,
            message=message,
            root_id=root_id,
            props=props,
        )

    async def post_reply(
        self, channel_id: str, root_id: str, message: str
    ) -> Result[PostDTO, IntegrationError]:
        return await self._client.create_post(
            channel_id=channel_id,
            message=message,
            root_id=root_id,
        )

    async def post_daily_digest(
        self, channel_id: str, title: str, summary: str, metrics_grid: list[dict[str, str]]
    ) -> Result[PostDTO, IntegrationError]:
        text = MarkdownBuilder().heading(f"📊 {title}", level=2).text(summary).build()
        builder = InteractiveAttachmentBuilder().title(title).text(summary).color("#0080FF")
        for item in metrics_grid:
            builder.add_field(item.get("title", ""), item.get("value", ""), short=True)

        attachment = builder.build()
        return await self._client.create_post(
            channel_id=channel_id,
            message=text,
            props={"attachments": [attachment]},
        )
