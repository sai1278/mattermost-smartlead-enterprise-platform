# Mattermost Slash Command Handler Microservice (`apps/command-handler`)

Processes Mattermost slash commands (`/warmup status`, `/warmup list`, `/warmup pause`, `/warmup resume`), validates authentication tokens, interacts with Smartlead via `tmmp-integrations-smartlead`, and formats responses using `tmmp-integrations-mattermost`.

## Endpoints

- **`POST /api/v1/commands/smartlead`**: Consumes `application/x-www-form-urlencoded` slash command payloads.
- **`GET /health`**: Health status probe.
