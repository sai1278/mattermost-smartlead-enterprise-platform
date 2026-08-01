"""Example launcher for Enterprise Analytics Service."""

from tmmp_analytics.config import AnalyticsConfig
from tmmp_analytics.main import create_app


def main() -> None:
    config = AnalyticsConfig(port=8003)
    app = create_app(config)
    print("Successfully initialized Enterprise Analytics Service:", app.title)


if __name__ == "__main__":
    main()
