"""In-Memory Repository Implementation for Analytics/Events Persistence."""

from __future__ import annotations

from tmmp_smartlead_sync.domain.entities import WarmupMetricsSnapshot
from tmmp_smartlead_sync.domain.events import WarmupEvent
from tmmp_smartlead_sync.domain.repository import WarmupRepositoryProtocol


class InMemoryWarmupRepository(WarmupRepositoryProtocol):
    """Thread-safe in-memory store decoupling business logic from DB implementations."""

    def __init__(self) -> None:
        self._snapshots: dict[int, list[WarmupMetricsSnapshot]] = {}
        self._events: list[WarmupEvent] = []

    async def save_snapshot(self, snapshot: WarmupMetricsSnapshot) -> None:
        if snapshot.account_id not in self._snapshots:
            self._snapshots[snapshot.account_id] = []
        self._snapshots[snapshot.account_id].append(snapshot)

    async def get_latest_snapshot(self, account_id: int) -> WarmupMetricsSnapshot | None:
        snapshots = self._snapshots.get(account_id, [])
        if not snapshots:
            return None
        return snapshots[-1]

    async def save_event(self, event: WarmupEvent) -> None:
        self._events.append(event)

    def get_all_events(self) -> list[WarmupEvent]:
        return list(self._events)
