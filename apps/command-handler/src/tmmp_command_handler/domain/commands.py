"""Domain Command Objects for Mattermost Slash Commands."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Command:
    user_id: str
    user_name: str
    channel_id: str
    team_id: str


@dataclass(frozen=True)
class WarmupStatusCommand(Command):
    mailbox: str = ""


@dataclass(frozen=True)
class WarmupListCommand(Command):
    pass


@dataclass(frozen=True)
class WarmupPauseCommand(Command):
    account_id: int = 0


@dataclass(frozen=True)
class WarmupResumeCommand(Command):
    account_id: int = 0


@dataclass(frozen=True)
class WarmupHelpCommand(Command):
    pass
