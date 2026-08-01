"""ClickHouse Data Transfer Objects."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class ClickHouseQueryResult:
    columns: list[str]
    rows: list[list[Any]] = field(default_factory=list)
