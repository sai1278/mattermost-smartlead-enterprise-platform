# Mattermost WebSocket Bot Microservice (`apps/bot`)

Production-grade AsyncIO Mattermost WebSocket Bot microservice. Consumes `tmmp-integrations-shared` and `tmmp-integrations-mattermost`.

## Core Features

- **Async WebSocket Listener**: Subscribes to real-time events via `MattermostWebSocketClient`.
- **Event Dispatcher**: Automatically detects `@mentions` and sends thread replies.
- **Daily Digest Publisher**: Generates interactive attachment summaries for channel broadcasts.
- **FastAPI Lifespan Integration**: Manages async listener start/stop lifecycle cleanly.
