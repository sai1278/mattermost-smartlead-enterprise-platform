"""Workflow Engine Application Services."""

from __future__ import annotations

from typing import Any

from tmmp_integrations_shared.dto import Result
from tmmp_integrations_shared.errors import IntegrationError
from tmmp_integrations_shared.logging import get_logger
from tmmp_workflow_engine.domain.models import (
    ApprovalGate,
    CampaignReadiness,
    EscalationPolicy,
    WorkflowInstance,
)
from tmmp_workflow_engine.infrastructure.flowable_repository import FlowableRepository

LOGGER = get_logger(__name__)


class WorkflowOrchestrator:
    """Orchestrates BPMN process lifecycle."""

    def __init__(self, repo: FlowableRepository) -> None:
        self._repo = repo

    async def start_workflow(
        self, process_key: str, variables: dict[str, Any]
    ) -> Result[WorkflowInstance, IntegrationError]:
        LOGGER.info("Starting workflow process key=%s", process_key)
        return await self._repo.start_warmup_process(process_key, variables)


class ApprovalService:
    """Manages multi-stage approvals."""

    async def approve_gate(
        self, process_id: str, approver: str
    ) -> Result[ApprovalGate, IntegrationError]:
        LOGGER.info("Approving gate process_id=%s approver=%s", process_id, approver)
        gate = ApprovalGate(
            gate_id="gate-101",
            process_id=process_id,
            step_name="Campaign Warmup Readiness",
            status="APPROVED",
            approver=approver,
        )
        return Result.ok(gate)

    async def reject_gate(
        self, process_id: str, approver: str
    ) -> Result[ApprovalGate, IntegrationError]:
        LOGGER.info("Rejecting gate process_id=%s approver=%s", process_id, approver)
        gate = ApprovalGate(
            gate_id="gate-101",
            process_id=process_id,
            step_name="Campaign Warmup Readiness",
            status="REJECTED",
            approver=approver,
        )
        return Result.ok(gate)


class EscalationService:
    """Handles escalation timers and policy triggers."""

    async def escalate_workflow(
        self, process_id: str
    ) -> Result[EscalationPolicy, IntegrationError]:
        LOGGER.warning("Escalating workflow process_id=%s", process_id)
        policy = EscalationPolicy(
            policy_id="esc-99",
            process_id=process_id,
            timeout_hours=24,
            escalation_level=2,
        )
        return Result.ok(policy)


class ReadinessGateService:
    """Evaluates deliverability readiness for campaign launch."""

    def evaluate_readiness(
        self, campaign_id: str, mailbox_count: int, avg_inbox_rate: float
    ) -> CampaignReadiness:
        is_ready = avg_inbox_rate >= 95.0 and mailbox_count >= 5
        return CampaignReadiness(
            campaign_id=campaign_id,
            mailbox_count=mailbox_count,
            avg_inbox_rate=avg_inbox_rate,
            ready=is_ready,
        )
