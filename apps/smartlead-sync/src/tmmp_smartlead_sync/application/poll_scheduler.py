"""Async Background Polling Scheduler."""

from __future__ import annotations

import asyncio
from contextlib import suppress

from tmmp_integrations_shared.logging import get_logger
from tmmp_smartlead_sync.application.warmup_service import WarmupSyncService

LOGGER = get_logger(__name__)


class PollingScheduler:
    """Periodic async task scheduler for polling Smartlead metrics."""

    def __init__(self, warmup_service: WarmupSyncService, interval_seconds: int = 300) -> None:
        self._service = warmup_service
        self._interval = interval_seconds
        self._running = False
        self._task: asyncio.Task[None] | None = None

    async def start(self) -> None:
        self._running = True
        self._task = asyncio.create_task(self._run_loop())
        LOGGER.info("Started PollingScheduler with interval %ds", self._interval)

    async def stop(self) -> None:
        self._running = False
        if self._task:
            self._task.cancel()
            with suppress(asyncio.CancelledError):
                await self._task
        LOGGER.info("Stopped PollingScheduler gracefully.")

    async def _run_loop(self) -> None:
        while self._running:
            try:
                await self._service.sync_all_accounts()
            except Exception as exc:
                LOGGER.error("Error during polling sync loop: %s", exc)
            await asyncio.sleep(self._interval)
