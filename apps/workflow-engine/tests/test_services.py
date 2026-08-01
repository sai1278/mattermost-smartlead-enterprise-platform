import asyncio
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock

from tmmp_integrations_shared.dto import Result
from tmmp_workflow_engine.application.services import (
    ApprovalService,
    ReadinessGateService,
    WorkflowOrchestrator,
)
from tmmp_workflow_engine.domain.models import WorkflowInstance


def test_workflow_services():
    repo = MagicMock()
    dummy_inst = WorkflowInstance("p1", "warmup_key", "ACTIVE", datetime.utcnow())
    repo.start_warmup_process = AsyncMock(return_value=Result.ok(dummy_inst))

    orchestrator = WorkflowOrchestrator(repo)
    approval_svc = ApprovalService()
    readiness_svc = ReadinessGateService()

    async def _test():
        res = await orchestrator.start_workflow("warmup_key", {"mailbox": "m1@d.com"})
        assert res.is_ok
        assert res.unwrap().process_id == "p1"

        app_res = await approval_svc.approve_gate("p1", "admin")
        assert app_res.is_ok
        assert app_res.unwrap().status == "APPROVED"

    asyncio.run(_test())

    ready_res = readiness_svc.evaluate_readiness("c1", 6, 96.0)
    assert ready_res.ready is True
