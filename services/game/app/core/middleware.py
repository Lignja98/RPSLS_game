"""Shared FastAPI middleware utilities (logging, tracing, …)."""

from __future__ import annotations

import uuid
from collections.abc import Awaitable, Callable

from fastapi import Request, Response
import structlog
from structlog.contextvars import bind_contextvars, clear_contextvars

__all__ = ["request_id_middleware"]


async def request_id_middleware(  # noqa: D401
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]],
) -> Response:
    """Attach *request_id* to structlog context and response headers.

    The middleware honours an incoming **X-Request-ID** header; when absent it
    generates a UUID4.  The id is injected into:

    1. *structlog* contextvars (so every subsequent `log.*` call in the same
       coroutine automatically includes it).
    2. The response headers - consumers can correlate requests ↔ logs easily.
    """

    # Reset any leftover context from previous tasks (important in tests)
    clear_contextvars()

    req_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    bind_contextvars(request_id=req_id, path=request.url.path, method=request.method)

    try:
        response = await call_next(request)
    except Exception:  # pragma: no cover – ensure we still log & respond
        # Log stacktrace with the bound request context (request_id, path…)
        structlog.get_logger().exception("Unhandled exception")

        from fastapi.responses import JSONResponse  # local import to avoid circular

        response = JSONResponse({"detail": "Internal Server Error"}, status_code=500)

    # Ensure correlation id is returned even on errors
    response.headers.setdefault("X-Request-ID", req_id)
    return response
