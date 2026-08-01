# Enterprise Analytics Microservice (`apps/analytics`)

Production-grade ClickHouse analytics ingestion and reporting microservice. Consumes `tmmp-integrations-shared` and `tmmp-integrations-clickhouse`.

## REST API Endpoints

- `GET /health`: Health status.
- `GET /analytics/warmup/{mailbox}`: Warmup stats for a specific mailbox.
- `GET /analytics/trends/{domain}`: 30-day deliverability trends.
- `GET /analytics/daily-summary`: Aggregate daily summary.
- `POST /analytics/events`: Batch event ingestion endpoint.
