import asyncio
from unittest.mock import AsyncMock, MagicMock

from tmmp_integrations_shared.dto import Result
from tmmp_integrations_smartlead import EmailAccount
from tmmp_smartlead_sync.application.warmup_service import WarmupSyncService
from tmmp_smartlead_sync.infrastructure.in_memory_repository import InMemoryWarmupRepository


def test_warmup_sync_service():
    smartlead_adapter = MagicMock()
    account = EmailAccount(id=1, from_email="acc1@test.com", is_warmup_enabled=True)
    smartlead_adapter.fetch_accounts = AsyncMock(return_value=Result.ok([account]))

    smartlead_adapter.fetch_metrics_snapshot = AsyncMock(
        return_value=Result.ok(
            MagicMock(
                account_id=1,
                email="acc1@test.com",
                sent_count=50,
                inbox_count=48,
                spam_count=1,
                bounce_count=1,
                inbox_rate=96.0,
                spam_rate=2.0,
                bounce_rate=2.0,
            )
        )
    )

    repo = InMemoryWarmupRepository()
    alert_dispatcher = MagicMock()
    alert_dispatcher.handle_event = AsyncMock()

    service = WarmupSyncService(smartlead_adapter, repo, alert_dispatcher)

    async def _test():
        await service.sync_all_accounts()
        assert alert_dispatcher.handle_event.called

    asyncio.run(_test())
