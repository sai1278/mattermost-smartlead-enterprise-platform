"""Smartlead Enterprise REST API Client."""

from __future__ import annotations

from typing import Any

from tmmp_integrations_shared.client import BaseAsyncHTTPClient
from tmmp_integrations_shared.dto import Result
from tmmp_integrations_shared.errors import IntegrationError

from tmmp_integrations_smartlead.auth import SmartleadAuth
from tmmp_integrations_smartlead.config import SmartleadConfig
from tmmp_integrations_smartlead.dto import Campaign, EmailAccount, WarmupAccount, WarmupStats
from tmmp_integrations_smartlead.endpoints import Routes
from tmmp_integrations_smartlead.telemetry import smartlead_span


class SmartleadClient(BaseAsyncHTTPClient):
    """SDK Client for interacting with Smartlead API v1."""

    def __init__(self, config: SmartleadConfig) -> None:
        auth = SmartleadAuth(api_key=config.api_key.get_secret_value())
        super().__init__(
            base_url=config.smartlead_api_url,
            auth_strategy=auth,
            service_name="smartlead-sdk",
        )
        self.config = config

    async def ping(self) -> Result[dict[str, Any], IntegrationError]:
        async with smartlead_span("ping"):
            return await self.get(Routes.CAMPAIGNS)

    async def list_campaigns(
        self,
        offset: int = 0,
        limit: int = 100,
    ) -> Result[list[Campaign], IntegrationError]:
        async with smartlead_span("list_campaigns"):
            res = await self.get(f"{Routes.CAMPAIGNS}?offset={offset}&limit={limit}")
            if res.is_ok:
                items = res.unwrap()
                if isinstance(items, list):
                    campaigns = [Campaign.model_validate(c) for c in items]
                    return Result.ok(campaigns)
                return Result.ok([])
            return Result.fail(res.error() or IntegrationError("list_campaigns failed"))

    async def get_campaign(self, campaign_id: int) -> Result[Campaign, IntegrationError]:
        async with smartlead_span("get_campaign", {"campaign_id": str(campaign_id)}):
            res = await self.get(Routes.campaign_details(campaign_id))
            if res.is_ok:
                return Result.ok(Campaign.model_validate(res.unwrap()))
            return Result.fail(res.error() or IntegrationError("get_campaign failed"))

    async def list_email_accounts(self) -> Result[list[EmailAccount], IntegrationError]:
        async with smartlead_span("list_email_accounts"):
            res = await self.get(Routes.EMAIL_ACCOUNTS)
            if res.is_ok:
                items = res.unwrap()
                if isinstance(items, list):
                    accounts = [EmailAccount.model_validate(a) for a in items]
                    return Result.ok(accounts)
                return Result.ok([])
            return Result.fail(res.error() or IntegrationError("list_email_accounts failed"))

    async def get_warmup_status(self, account_id: int) -> Result[WarmupAccount, IntegrationError]:
        async with smartlead_span("get_warmup_status", {"account_id": str(account_id)}):
            res = await self.get(Routes.warmup_status(account_id))
            if res.is_ok:
                return Result.ok(WarmupAccount.model_validate(res.unwrap()))
            return Result.fail(res.error() or IntegrationError("get_warmup_status failed"))

    async def get_warmup_stats(self, account_id: int) -> Result[WarmupStats, IntegrationError]:
        async with smartlead_span("get_warmup_stats", {"account_id": str(account_id)}):
            res = await self.get(Routes.warmup_stats(account_id))
            if res.is_ok:
                return Result.ok(WarmupStats.model_validate(res.unwrap()))
            return Result.fail(res.error() or IntegrationError("get_warmup_stats failed"))

    async def pause_warmup(self, account_id: int) -> Result[dict[str, Any], IntegrationError]:
        async with smartlead_span("pause_warmup", {"account_id": str(account_id)}):
            return await self.post(Routes.warmup_pause(account_id), json_data={})

    async def resume_warmup(self, account_id: int) -> Result[dict[str, Any], IntegrationError]:
        async with smartlead_span("resume_warmup", {"account_id": str(account_id)}):
            return await self.post(Routes.warmup_resume(account_id), json_data={})
