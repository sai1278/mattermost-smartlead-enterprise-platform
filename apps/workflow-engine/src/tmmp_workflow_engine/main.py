"""FastAPI Workflow Engine Microservice Entrypoint."""

from __future__ import annotations

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from tmmp_integrations_flowable import FlowableClient, FlowableConfig

from tmmp_workflow_engine.api.router import router, set_workflow_services
from tmmp_workflow_engine.application.services import (
    ApprovalService,
    EscalationService,
    WorkflowOrchestrator,
)
from tmmp_workflow_engine.config import WorkflowEngineConfig
from tmmp_workflow_engine.infrastructure.flowable_repository import FlowableRepository


def create_app(config: WorkflowEngineConfig | None = None) -> FastAPI:
    _ = config or WorkflowEngineConfig()

    flowable_client = FlowableClient(FlowableConfig())
    repo = FlowableRepository(flowable_client)

    orchestrator = WorkflowOrchestrator(repo)
    approval_svc = ApprovalService()
    escalation_svc = EscalationService()

    set_workflow_services(orchestrator, approval_svc, escalation_svc)

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
        yield
        await flowable_client.close()

    app = FastAPI(
        title="Flowable Enterprise Workflow Engine Microservice",
        version="0.1.0",
        lifespan=lifespan,
    )
    app.include_router(router)

    @app.get("/health")
    async def health() -> dict[str, str]:
        return {"status": "UP", "service": "workflow-engine"}

    return app


app = create_app()
