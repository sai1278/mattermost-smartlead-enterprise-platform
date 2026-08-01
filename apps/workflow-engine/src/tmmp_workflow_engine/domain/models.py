"""Domain Models for Workflow Engine."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass(frozen=True)
class WorkflowInstance:
    process_id: str
    key: str
    state: str
    created_at: datetime
    variables: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ApprovalGate:
    gate_id: str
    process_id: str
    step_name: str
    status: str
    approver: str | None = None


@dataclass(frozen=True)
class EscalationPolicy:
    policy_id: str
    process_id: str
    timeout_hours: int
    escalation_level: int


@dataclass(frozen=True)
class CampaignReadiness:
    campaign_id: str
    mailbox_count: int
    avg_inbox_rate: float
    ready: bool


@dataclass(frozen=True)
class WorkflowEvent:
    event_type: str
    payload: dict[str, Any]
