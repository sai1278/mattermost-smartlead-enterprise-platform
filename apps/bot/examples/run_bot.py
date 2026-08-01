"""Example script initializing Mattermost Bot App."""

from tmmp_mattermost_bot.config import BotConfig
from tmmp_mattermost_bot.main import create_app


def main() -> None:
    config = BotConfig(port=8002)
    app = create_app(config)
    print("Successfully initialized Mattermost Bot Microservice App:", app.title)


if __name__ == "__main__":
    main()
