"""Warmup Sync Service Application Orchestrator."""

from __future__ import annotations

from tmmp_integrations_shared.logging import get_logger
from tmmp_smartlead_sync.application.alert_service import AlertDispatcher
from tmmp_smartlead_sync.domain.policies import WarmupEvaluationPolicy
from tmmp_smartlead_sync.domain.repository import WarmupRepositoryProtocol
from tmmp_smartlead_sync.infrastructure.smartlead_adapter import SmartleadAdapter

LOGGER = get_logger(__name__)


class WarmupSyncService:
    """Application Service orchestrating metrics sync, evaluation, persistence, and alerts."""

    def __init__(
        self,
        smartlead_adapter: SmartleadAdapter,
        repository: WarmupRepositoryProtocol,
        alert_dispatcher: AlertDispatcher,
    ) -> None:
        self._smartlead = smartlead_adapter
        self._repository = repository
        self._alert = alert_dispatcher

    async def sync_all_accounts(self) -> None:
        LOGGER.info("Starting sync cycle for all Smartlead warmup accounts...")
        acc_res = await self._smartlead.fetch_accounts()
        if acc_res.is_fail:
            LOGGER.error("Failed to list email accounts: %s", acc_res.error())
            return

        accounts = acc_res.unwrap()
        for acc in accounts:
            if not acc.is_warmup_enabled:
                continue

            snap_res = await self._smartlead.fetch_metrics_snapshot(acc)
            if snap_res.is_fail:
                LOGGER.warning(
                    "Failed metrics snapshot for %s: %s",
                    acc.from_email,
                    snap_res.error(),
                )
                continue

            snapshot = snap_res.unwrap()
            await self._repository.save_snapshot(snapshot)

            event = WarmupEvaluationPolicy.evaluate(snapshot)
            await self._repository.save_event(event)
            await self._alert.handle_event(event)

        LOGGER.info("Completed sync cycle for %d accounts.", len(accounts))
