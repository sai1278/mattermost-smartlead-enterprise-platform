"""Flowable Repository Adapter interfacing with Flowable SDK."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from tmmp_integrations_flowable import FlowableClient
from tmmp_integrations_shared.dto import Result
from tmmp_integrations_shared.errors import IntegrationError
from tmmp_workflow_engine.domain.models import WorkflowInstance


class FlowableRepository:
    """Repository executing BPMN process operations via Flowable SDK."""

    def __init__(self, client: FlowableClient) -> None:
        self._client = client

    async def start_warmup_process(
        self, process_key: str, variables: dict[str, Any]
    ) -> Result[WorkflowInstance, IntegrationError]:
        res = await self._client.start_process_instance(process_key, variables)
        if res.is_fail:
            err = res.error()
            return Result.fail(err or IntegrationError(message="Process start failed"))

        inst = res.unwrap()
        workflow_inst = WorkflowInstance(
            process_id=inst.id,
            key=process_key,
            state="ACTIVE" if not inst.ended else "COMPLETED",
            created_at=datetime.utcnow(),
            variables=variables,
        )
        return Result.ok(workflow_inst)
