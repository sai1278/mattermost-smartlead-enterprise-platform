"""Example script initializing and verifying Smartlead Sync Worker."""

from tmmp_smartlead_sync.config import SyncWorkerConfig
from tmmp_smartlead_sync.main import create_app


def main() -> None:
    config = SyncWorkerConfig(sync_interval_seconds=60)
    app = create_app(config)
    print("Successfully initialized Smartlead Sync Microservice App:", app.title)


if __name__ == "__main__":
    main()
