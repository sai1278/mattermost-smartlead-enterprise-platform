"""ClickHouse HTTP/SQL Async Client."""

from __future__ import annotations

from typing import Any

import httpx
from tmmp_integrations_shared.dto import Result
from tmmp_integrations_shared.errors import IntegrationError
from tmmp_integrations_shared.logging import get_logger

from tmmp_integrations_clickhouse.config import ClickHouseConfig
from tmmp_integrations_clickhouse.dto import ClickHouseQueryResult

LOGGER = get_logger(__name__)


class ClickHouseClient:
    """Async client for executing SQL queries and batch inserts against ClickHouse."""

    def __init__(self, config: ClickHouseConfig | None = None) -> None:
        self._config = config or ClickHouseConfig()
        self._http = httpx.AsyncClient(
            base_url=self._config.url,
            auth=(self._config.user, self._config.password.get_secret_value()),
            timeout=self._config.timeout_seconds,
        )

    async def close(self) -> None:
        await self._http.aclose()

    async def execute_query(self, query: str) -> Result[ClickHouseQueryResult, IntegrationError]:
        try:
            params = {"database": self._config.database, "default_format": "JSONCompact"}
            response = await self._http.post("/", content=query, params=params)
            if response.status_code != 200:
                return Result.fail(
                    IntegrationError(
                        message=f"ClickHouse query failed ({response.status_code}): {response.text}"
                    )
                )
            data = response.json()
            meta = [col.get("name", "") for col in data.get("meta", [])]
            rows = data.get("data", [])
            return Result.ok(ClickHouseQueryResult(columns=meta, rows=rows))
        except Exception as exc:
            LOGGER.error("ClickHouse query exception: %s", exc)
            return Result.fail(IntegrationError(message=f"ClickHouse connection error: {exc}"))

    async def insert_rows(
        self, table: str, columns: list[str], rows: list[list[Any]]
    ) -> Result[bool, IntegrationError]:
        if not rows:
            return Result.ok(True)

        cols_str = ", ".join(columns)
        query = f"INSERT INTO {table} ({cols_str}) FORMAT JSONCompactEachRow\n"
        try:
            params = {"database": self._config.database}
            response = await self._http.post("/", content=query, params=params)
            if response.status_code != 200:
                return Result.fail(IntegrationError(message=f"Insert failed: {response.text}"))
            return Result.ok(True)
        except Exception as exc:
            LOGGER.error("ClickHouse insert exception: %s", exc)
            return Result.fail(IntegrationError(message=f"ClickHouse insert exception: {exc}"))
