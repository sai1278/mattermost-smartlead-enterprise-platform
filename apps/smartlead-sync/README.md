# Smartlead Sync Business Microservice (`apps/smartlead-sync`)

First business microservice of the Mattermost ↔ Smartlead Warmup Platform. Reuses `tmmp-integrations-shared`, `tmmp-integrations-mattermost`, and `tmmp-integrations-smartlead`.

## Core Responsibilities

- **Periodic Smartlead Polling**: `PollingScheduler` periodically fetches mailbox warmup statistics.
- **Webhook Endpoint**: `POST /api/v1/webhooks/smartlead` handles real-time Smartlead events with HMAC signature validation.
- **Domain Event Evaluation**: `WarmupEvaluationPolicy` evaluates metrics and emits domain events (`WarmupHealthy`, `WarmupWarning`, `WarmupCritical`, `CampaignReady`).
- **Mattermost Notifications**: `MattermostAlertAdapter` formats interactive attachment alerts to Mattermost channels.
- **Persistence Abstraction**: `WarmupRepositoryProtocol` decouples business logic from persistence databases.
