"""Request Context and Correlation ID Propagation."""

from __future__ import annotations

import contextvars
import uuid
from dataclasses import dataclass, field
from typing import Any

_CORRELATION_ID_CTX: contextvars.ContextVar[str | None] = contextvars.ContextVar(
    "correlation_id", default=None
)


def get_correlation_id() -> str:
    """Retrieve current correlation ID or generate a new UUID4."""
    cid = _CORRELATION_ID_CTX.get()
    if not cid:
        cid = str(uuid.uuid4())
        _CORRELATION_ID_CTX.set(cid)
    return cid


def set_correlation_id(correlation_id: str) -> None:
    """Set correlation ID for current async context."""
    _CORRELATION_ID_CTX.set(correlation_id)


@dataclass
class RequestContext:
    """Immutable request context for cross-cutting tracing and logging."""

    correlation_id: str = field(default_factory=get_correlation_id)
    tenant_id: str | None = None
    user_id: str | None = None
    extra: dict[str, Any] = field(default_factory=dict)
