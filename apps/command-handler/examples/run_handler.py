"""Example script initializing and verifying Command Handler Microservice."""

from tmmp_command_handler.config import CommandHandlerConfig
from tmmp_command_handler.main import create_app


def main() -> None:
    config = CommandHandlerConfig(port=8001)
    app = create_app(config)
    print("Successfully initialized Command Handler Microservice App:", app.title)


if __name__ == "__main__":
    main()
