# Flowable Enterprise Workflow Engine Microservice (`apps/workflow-engine`)

Enterprise Workflow Orchestration Service consuming Flowable BPMN Engine. Consumes `tmmp-integrations-shared`, `tmmp-integrations-flowable`, `tmmp-integrations-mattermost`, and `tmmp-integrations-clickhouse`.

## REST API Endpoints

- `GET /health`: Microservice health check.
- `POST /workflow/start`: Start a new BPMN workflow instance.
- `POST /workflow/approve`: Approve a workflow approval gate.
- `POST /workflow/reject`: Reject a workflow approval gate.
- `POST /workflow/escalate`: Trigger escalation policy.
- `GET /workflow/{process_id}`: Query workflow instance status.
