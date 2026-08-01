"""Flowable Data Transfer Objects."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class ProcessDefinitionDTO:
    id: str
    key: str
    name: str
    version: int


@dataclass(frozen=True)
class ProcessInstanceDTO:
    id: str
    process_definition_id: str
    ended: bool
    suspended: bool
    variables: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class TaskDTO:
    id: str
    name: str
    assignee: str | None
    process_instance_id: str
    create_time: str
