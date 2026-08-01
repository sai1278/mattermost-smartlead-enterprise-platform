"""Smartlead Async Endpoint Paginator."""

from __future__ import annotations

from collections.abc import AsyncGenerator
from typing import Any, TypeVar

from tmmp_integrations_shared.dto import BaseDTO, Result
from tmmp_integrations_shared.errors import IntegrationError

T = TypeVar("T", bound=BaseDTO)


class SmartleadPaginator:
    """Async iterator helper for paginated Smartlead REST endpoints."""

    @staticmethod
    async def iterate_pages(
        fetch_func: Any,
        page_size: int = 100,
    ) -> AsyncGenerator[list[dict[str, Any]], None]:
        offset = 0
        while True:
            res: Result[list[dict[str, Any]], IntegrationError] = await fetch_func(
                offset=offset, limit=page_size
            )
            if res.is_fail or not res.unwrap():
                break

            items = res.unwrap()
            yield items

            if len(items) < page_size:
                break
            offset += page_size
