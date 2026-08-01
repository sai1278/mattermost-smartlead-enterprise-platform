from datetime import datetime

from tmmp_workflow_engine.domain.models import ApprovalGate, CampaignReadiness, WorkflowInstance


def test_workflow_domain_models():
    now = datetime.utcnow()
    inst = WorkflowInstance("proc-1", "warmup_approval", "ACTIVE", now, {"mailbox": "m1@d.com"})
    assert inst.process_id == "proc-1"
    assert inst.state == "ACTIVE"

    gate = ApprovalGate("g-1", "proc-1", "Readiness Gate", "APPROVED", "mgr1")
    assert gate.status == "APPROVED"

    readiness = CampaignReadiness("camp-1", 10, 96.5, True)
    assert readiness.ready is True
