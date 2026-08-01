"""Feature Flag Provider Interface and Implementation."""

from __future__ import annotations

from abc import ABC, abstractmethod


class FeatureFlagProvider(ABC):
    """Abstract interface for feature flag evaluate providers."""

    @abstractmethod
    async def is_enabled(self, flag_name: str, default: bool = False) -> bool:
        """Check if feature flag is enabled."""


class InMemoryFeatureFlagProvider(FeatureFlagProvider):
    """In-memory feature flag provider for development and testing."""

    def __init__(self, flags: dict[str, bool] | None = None) -> None:
        self._flags = flags or {}

    async def is_enabled(self, flag_name: str, default: bool = False) -> bool:
        return self._flags.get(flag_name, default)

    def set_flag(self, flag_name: str, enabled: bool) -> None:
        self._flags[flag_name] = enabled
