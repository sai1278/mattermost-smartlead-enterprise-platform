"""Async Batch Writer buffering events before flushing to ClickHouse."""

from __future__ import annotations

import asyncio
from typing import Any

from tmmp_integrations_clickhouse import ClickHouseClient
from tmmp_integrations_shared.logging import get_logger

LOGGER = get_logger(__name__)


class BatchWriter:
    """Buffers domain metrics rows in memory and flushes in batches."""

    def __init__(
        self,
        client: ClickHouseClient,
        batch_size: int = 100,
        flush_interval: float = 5.0,
    ) -> None:
        self._client = client
        self._batch_size = batch_size
        self._flush_interval = flush_interval
        self._buffer: list[list[Any]] = []
        self._lock = asyncio.Lock()

    @property
    def buffer_count(self) -> int:
        return len(self._buffer)

    async def add_row(self, row: list[Any]) -> None:
        async with self._lock:
            self._buffer.append(row)
            if len(self._buffer) >= self._batch_size:
                await self._flush_unlocked()

    async def flush(self) -> None:
        async with self._lock:
            await self._flush_unlocked()

    async def _flush_unlocked(self) -> None:
        if not self._buffer:
            return
        rows_to_insert = list(self._buffer)
        self._buffer.clear()

        cols = ["mailbox", "timestamp", "sent", "inbox", "spam", "replies"]
        res = await self._client.insert_rows("warmup_metrics", cols, rows_to_insert)
        if res.is_fail:
            LOGGER.error("Failed to flush analytics batch: %s", res.error())
        else:
            LOGGER.info("Successfully flushed %d metrics rows to ClickHouse", len(rows_to_insert))
