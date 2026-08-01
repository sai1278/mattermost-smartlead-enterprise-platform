# Mattermost Enterprise Integration SDK (`tmmp-integrations-mattermost`)

Production-grade, typed Python SDK for Mattermost REST API v4 and WebSocket event streaming. Reuses `tmmp-integrations-shared` for resilience, telemetry, metrics, and monadic error handling.

## Components Included

- **`MattermostClient`**: Async HTTP REST client (Posts, Channels, Users, Teams, Direct Messages).
- **`MattermostWebSocketClient`**: Async WebSocket client for listening to real-time events.
- **`MarkdownBuilder`**: Fluent API for constructing formatted markdown messages.
- **`InteractiveAttachmentBuilder`**: Builder for interactive Slack-compatible attachments & buttons.
- **`MattermostHealthCheck`**: Health check implementation checking `/api/v4/system/ping`.
- **`SlashCommandPayload` & `SlashCommandResponse`**: Typed DTOs for slash command handling.

## Usage Example

```python
import asyncio
from pydantic import SecretStr
from tmmp_integrations_mattermost import MattermostClient, MattermostConfig, MarkdownBuilder

async def main():
    config = MattermostConfig(
        mattermost_url="http://localhost:8065",
        bot_token=SecretStr("bot-token-here"),
    )
    client = MattermostClient(config)

    msg = MarkdownBuilder().heading("Alert").bold("System Status:").text("All healthy.").build()
    result = await client.create_post(channel_id="channel-id-123", message=msg)

    if result.is_ok:
        post = result.unwrap()
        print("Post created with ID:", post.id)
    else:
        print("Failed to create post:", result.error())

    await client.close()

if __name__ == "__main__":
    asyncio.run(main())
```
