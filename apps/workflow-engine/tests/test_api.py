from datetime import datetime
from unittest.mock import AsyncMock, MagicMock

from fastapi.testclient import TestClient
from tmmp_integrations_shared.dto import Result
from tmmp_workflow_engine.api.router import set_workflow_services
from tmmp_workflow_engine.domain.models import WorkflowInstance
from tmmp_workflow_engine.main import create_app


def test_workflow_health_endpoint():
    app = create_app()
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["service"] == "workflow-engine"


def test_workflow_start_endpoint():
    orchestrator = MagicMock()
    approval_svc = MagicMock()
    escalation_svc = MagicMock()

    dummy_inst = WorkflowInstance("proc-101", "warmup_approval", "ACTIVE", datetime.utcnow())
    orchestrator.start_workflow = AsyncMock(return_value=Result.ok(dummy_inst))

    set_workflow_services(orchestrator, approval_svc, escalation_svc)

    app = create_app()
    set_workflow_services(orchestrator, approval_svc, escalation_svc)

    client = TestClient(app)
    response = client.post("/workflow/start", json={"process_key": "warmup_approval"})
    assert response.status_code == 200
    assert response.json()["process_id"] == "proc-101"
    assert response.json()["state"] == "ACTIVE"
