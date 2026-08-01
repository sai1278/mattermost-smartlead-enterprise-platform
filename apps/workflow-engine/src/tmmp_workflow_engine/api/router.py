"""REST API Router for Workflow Engine Microservice."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from tmmp_workflow_engine.application.services import (
    ApprovalService,
    EscalationService,
    WorkflowOrchestrator,
)

router = APIRouter(prefix="/workflow", tags=["workflow"])

_orchestrator: WorkflowOrchestrator | None = None
_approval_svc: ApprovalService | None = None
_escalation_svc: EscalationService | None = None


def set_workflow_services(
    orchestrator: WorkflowOrchestrator,
    approval: ApprovalService,
    escalation: EscalationService,
) -> None:
    global _orchestrator, _approval_svc, _escalation_svc
    _orchestrator = orchestrator
    _approval_svc = approval
    _escalation_svc = escalation


class StartWorkflowPayload(BaseModel):
    process_key: str
    variables: dict[str, Any] = {}


class ActionPayload(BaseModel):
    process_id: str
    approver: str = "admin"


@router.post("/start")
async def start_workflow(payload: StartWorkflowPayload) -> dict[str, Any]:
    if not _orchestrator:
        raise HTTPException(status_code=500, detail="Service uninitialized")
    res = await _orchestrator.start_workflow(payload.process_key, payload.variables)
    if res.is_fail:
        err = res.error()
        msg = err.message if err else "Workflow start failed"
        raise HTTPException(status_code=500, detail=msg)
    inst = res.unwrap()
    return {"process_id": inst.process_id, "state": inst.state}


@router.post("/approve")
async def approve_workflow(payload: ActionPayload) -> dict[str, Any]:
    if not _approval_svc:
        raise HTTPException(status_code=500, detail="Service uninitialized")
    res = await _approval_svc.approve_gate(payload.process_id, payload.approver)
    if res.is_fail:
        err = res.error()
        msg = err.message if err else "Approval failed"
        raise HTTPException(status_code=500, detail=msg)
    gate = res.unwrap()
    return {"gate_id": gate.gate_id, "status": gate.status}


@router.post("/reject")
async def reject_workflow(payload: ActionPayload) -> dict[str, Any]:
    if not _approval_svc:
        raise HTTPException(status_code=500, detail="Service uninitialized")
    res = await _approval_svc.reject_gate(payload.process_id, payload.approver)
    if res.is_fail:
        err = res.error()
        msg = err.message if err else "Rejection failed"
        raise HTTPException(status_code=500, detail=msg)
    gate = res.unwrap()
    return {"gate_id": gate.gate_id, "status": gate.status}


@router.post("/escalate")
async def escalate_workflow(payload: ActionPayload) -> dict[str, Any]:
    if not _escalation_svc:
        raise HTTPException(status_code=500, detail="Service uninitialized")
    res = await _escalation_svc.escalate_workflow(payload.process_id)
    if res.is_fail:
        err = res.error()
        msg = err.message if err else "Escalation failed"
        raise HTTPException(status_code=500, detail=msg)
    policy = res.unwrap()
    return {"policy_id": policy.policy_id, "level": policy.escalation_level}


@router.get("/{process_id}")
async def get_workflow(process_id: str) -> dict[str, Any]:
    return {"process_id": process_id, "state": "ACTIVE"}
