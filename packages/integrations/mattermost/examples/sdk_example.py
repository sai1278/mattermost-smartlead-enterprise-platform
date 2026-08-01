"""Example usage of Mattermost Enterprise SDK."""

import asyncio

from pydantic import SecretStr
from tmmp_integrations_mattermost import (
    InteractiveAttachmentBuilder,
    MarkdownBuilder,
    MattermostClient,
    MattermostConfig,
)


async def run_example() -> None:
    config = MattermostConfig(
        mattermost_url="http://localhost:8065",
        bot_token=SecretStr("example-bot-token"),
    )
    client = MattermostClient(config)

    msg = (
        MarkdownBuilder()
        .heading("Warmup Status Report", level=2)
        .bold("Target Pool:")
        .text("Smartlead Enterprise")
        .newline()
        .bullet("Active mailboxes: 42")
        .bullet("Deliverability: 98.4%")
        .build()
    )

    attachment = (
        InteractiveAttachmentBuilder()
        .title("Quick Action")
        .color("#0080FF")
        .add_button("view_dash", "Open Dashboard", "https://dashboard.example.com")
        .build()
    )

    print("Created message payload:")
    print(msg)
    print("Created attachment payload:", attachment)

    await client.close()


if __name__ == "__main__":
    asyncio.run(run_example())
