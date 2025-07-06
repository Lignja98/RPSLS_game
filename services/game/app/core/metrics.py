from __future__ import annotations

"""Prometheus metrics specific to the game service."""

from prometheus_client import Counter

# ---------------------------------------------------------------------------
# Custom counters
# ---------------------------------------------------------------------------

AI_MODE_TOTAL = Counter(
    "rpsls_ai_mode_total",
    "Total number of rounds played per AI mode",
    labelnames=["mode"],
)

AI_OUTCOME_TOTAL = Counter(
    "rpsls_ai_outcome_total",
    "AI outcomes by mode (win/lose/tie from player perspective)",
    labelnames=["mode", "outcome"],
)
