"""Application-wide logging helpers.

Provides a single `init_logging()` function that must be called **once** as
early as possible (ideally before the FastAPI app is instantiated).  The
function configures:

* Standard library `logging` - root logger outputs JSON to *stdout*.
* [structlog](https://www.structlog.org/) - adds context-vars support and handy
  processors (timestamp, level, exception stack-traces, etc.).

The log-level is controlled with the environment variable `LOG_LEVEL` (DEBUG,
INFO, WARNING, …).  If it's not set we fall back to `DEBUG` when the global
`DEBUG` env-var is truthy, otherwise to `INFO`.
"""

from __future__ import annotations

import logging
import os
import sys
from typing import Final

import structlog

__all__: Final = ["init_logging"]

# Internal flag so repeated init_logging() calls are no-ops (unless force_reinit=True)
_CONFIGURED: bool = False


def _detect_level() -> int:
    """Return an *int* log level from environment variables."""

    # Highest priority – explicit LOG_LEVEL
    log_level = os.getenv("LOG_LEVEL")
    if log_level:
        return getattr(logging, log_level.upper(), logging.INFO)

    # Fallback – respect generic DEBUG flag (docker-compose, etc.)
    debug_flag = os.getenv("DEBUG", "0").lower()
    if debug_flag in {"1", "true", "yes"}:  # pragmatically truthy
        return logging.DEBUG

    return logging.INFO


def init_logging(force_reinit: bool = False) -> None:  # pragma: no cover
    """Configure stdlib + structlog global settings.

    Calling `init_logging()` more than once doesn't hurt but does nothing by
    default.  Pass *force_reinit=True* to rebuild the configuration (useful in
    e.g. unit tests that monkey-patch processors).
    """

    global _CONFIGURED

    if _CONFIGURED and not force_reinit:
        return  # already configured – skip

    level = _detect_level()

    # ------------------------------------------------------------------
    # Stdlib logging – minimal handler writing raw messages to stdout.
    # The *actual* formatting happens in structlog's JSONRenderer below.
    # ------------------------------------------------------------------
    logging.basicConfig(
        level=level,
        format="%(message)s",  # structlog already produces JSON strings
        stream=sys.stdout,
        force=True,  # override possible prior basicConfig calls (e.g. Alembic)
    )

    # ------------------------------------------------------------------
    # structlog configuration
    # ------------------------------------------------------------------
    structlog.configure(
        wrapper_class=structlog.make_filtering_bound_logger(level),
        logger_factory=structlog.PrintLoggerFactory(),
        processors=[
            structlog.contextvars.merge_contextvars,  # include contextvars (e.g. request-id)
            structlog.processors.TimeStamper(fmt="iso", key="ts"),
            structlog.processors.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer(),  # final output – emits JSON per line
        ],
        cache_logger_on_first_use=True,
    )

    _CONFIGURED = True
