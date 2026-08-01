"""Smartlead Infrastructure Adapter for Command Handler."""

from __future__ import annotations

from typing import Any

from tmmp_integrations_shared.dto import Result
from tmmp_integrations_shared.errors import IntegrationError
from tmmp_integrations_smartlead import EmailAccount, SmartleadClient, WarmupAccount
from tmmp_integrations_smartlead.dto import WarmupStats


class SmartleadCommandAdapter:
    """Adapter facilitating Smartlead SDK calls for slash commands."""

    def __init__(self, client: SmartleadClient) -> None:
        self._client = client

    async def get_accounts(self) -> Result[list[EmailAccount], IntegrationError]:
        return await self._client.list_email_accounts()

    async def get_warmup_status(self, account_id: int) -> Result[WarmupAccount, IntegrationError]:
        return await self._client.get_warmup_status(account_id)

    async def get_warmup_stats(self, account_id: int) -> Result[WarmupStats, IntegrationError]:
        return await self._client.get_warmup_stats(account_id)

    async def pause_warmup(self, account_id: int) -> Result[dict[str, Any], IntegrationError]:
        return await self._client.pause_warmup(account_id)

    async def resume_warmup(self, account_id: int) -> Result[dict[str, Any], IntegrationError]:
        return await self._client.resume_warmup(account_id)
