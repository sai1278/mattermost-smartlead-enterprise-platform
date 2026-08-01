# Changelog

All notable changes to the Mattermost ↔ Smartlead Enterprise Platform will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-08-01

### Added
- **Clean Monorepo Workspace Foundation:** UV workspace root with 5 SDKs (`packages/integrations/*`) and 5 Business Microservices (`apps/*`).
- **Shared Integration SDK (`tmmp-integrations-shared`):** Circuit breakers, retries with exponential backoff, rate limiting, and OTel tracing.
- **Mattermost SDK (`tmmp-integrations-mattermost`):** Async HTTP REST API v4 client, WebSocket real-time event client, rich Markdown builder, SlashCommand DTOs.
- **Smartlead SDK (`tmmp-integrations-smartlead`):** Campaign, mailbox, warmup analytics, and webhook ingestion SDK.
- **ClickHouse SDK (`tmmp-integrations-clickhouse`):** High-throughput columnar telemetry ingestion client.
- **Flowable SDK (`tmmp-integrations-flowable`):** BPMN engine REST client for process instance and task management.
- **Smartlead Sync Worker (`apps/smartlead-sync`):** Polling, webhook processing, Redis domain event publishing.
- **Command Handler Service (`apps/command-handler`):** Mattermost slash command service (`/warmup`).
- **WebSocket Bot Service (`apps/bot`):** Real-time proactive channel alert dispatch.
- **Analytics Ingestion Service (`apps/analytics`):** Metric ingestion, ClickHouse storage, deliverability tracking.
- **Workflow Engine Microservice (`apps/workflow-engine`):** Flowable BPMN workflow orchestration, approval gates, escalation policies.
- **Enterprise Platform Infrastructure:** `docker-compose.enterprise.yml`, `.env.example`, OpenTelemetry Collector, Prometheus, Grafana, Alertmanager.
- **Security & Chaos Resiliency:** Bandit, Semgrep, Trivy, Gitleaks, CycloneDX SBOM, Chaos Mesh, LitmusChaos manifests.

### Preserved
- **100% Parser Isolation:** `apps/parser` remains completely isolated; all 50 parser unit tests passing with 90.22% coverage.
