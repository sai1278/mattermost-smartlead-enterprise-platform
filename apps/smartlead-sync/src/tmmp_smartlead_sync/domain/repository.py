"""Repository Protocols (Dependency Inversion Boundary)."""

from __future__ import annotations

from typing import Protocol

from tmmp_smartlead_sync.domain.entities import WarmupMetricsSnapshot
from tmmp_smartlead_sync.domain.events import WarmupEvent


class WarmupRepositoryProtocol(Protocol):
    """Abstract persistence repository for warmup metrics and domain events."""

    async def save_snapshot(self, snapshot: WarmupMetricsSnapshot) -> None: ...

    async def get_latest_snapshot(self, account_id: int) -> WarmupMetricsSnapshot | None: ...

    async def save_event(self, event: WarmupEvent) -> None: ...
