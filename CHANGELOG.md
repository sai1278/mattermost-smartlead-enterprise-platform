# Changelog

All notable changes to the Mattermost ↔ Smartlead Enterprise Platform will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0](https://github.com/sai1278/mattermost-smartlead-enterprise-platform/compare/v0.1.0...v0.2.0) (2026-08-01)


### Features

* add migration validation, observability, security hardening and CI fixes ([7b161db](https://github.com/sai1278/mattermost-smartlead-enterprise-platform/commit/7b161db28f5b31ee7a7f46aad1228a85eb64aabb))
* harden Teams-to-Mattermost migration platform ([43ba4a4](https://github.com/sai1278/mattermost-smartlead-enterprise-platform/commit/43ba4a4e6bceb33049e281147edd3588aaf5bd11))
* **platform:** release Mattermost ↔ Smartlead Enterprise Platform v1.0.0-GA ([5303ffd](https://github.com/sai1278/mattermost-smartlead-enterprise-platform/commit/5303ffda40bbc4883fae2189b39c112efda54b2a))
* production hardening and migration reliability improvements ([adf4ad7](https://github.com/sai1278/mattermost-smartlead-enterprise-platform/commit/adf4ad745ca2c6f54a1945f0a55cdf3570a98805))
* production hardening, migration improvements, testing and observability enhancements ([b533dd3](https://github.com/sai1278/mattermost-smartlead-enterprise-platform/commit/b533dd34e7bf65ffecf2f97b5a94808637def0e2))
* production hardening, observability and kubernetes improvements ([63f65e4](https://github.com/sai1278/mattermost-smartlead-enterprise-platform/commit/63f65e4e1b4e1ab0c5963907af539ff1893fd6c6))
* production-grade Teams to Mattermost migration platform ([09b2b30](https://github.com/sai1278/mattermost-smartlead-enterprise-platform/commit/09b2b3073a32a9bb5af6240d9163a98f46fff146))
* release v1.0.0-GA Mattermost ↔ Smartlead Enterprise Platform ([fefe394](https://github.com/sai1278/mattermost-smartlead-enterprise-platform/commit/fefe3948aff0461d5cf16e0628abe5e31f4efd64))


### Bug Fixes

* break long lines to pass ruff linting ([76078bf](https://github.com/sai1278/mattermost-smartlead-enterprise-platform/commit/76078bf18a662cd814d969ce74c5730c6f0be7bb))
* exclude archived docs from Ruff formatting checks ([96d166c](https://github.com/sai1278/mattermost-smartlead-enterprise-platform/commit/96d166cfbe338609be7be98341de239ad5162249))
* Remove pinned Docker image digest that no longer exists ([6cec975](https://github.com/sai1278/mattermost-smartlead-enterprise-platform/commit/6cec975431763dc8394dd4bd981100201afd1733))

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
