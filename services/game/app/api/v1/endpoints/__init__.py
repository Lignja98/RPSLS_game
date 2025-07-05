from __future__ import annotations

"""Re-export all endpoint routers."""

from importlib import import_module
from types import ModuleType
from collections.abc import Sequence

from fastapi import APIRouter


def _collect_routers() -> list[APIRouter]:
    routers: list[APIRouter] = []
    for name in ("choices", "play", "history", "health"):
        module: ModuleType = import_module(f"app.api.v1.endpoints.{name}")
        router: APIRouter | None = getattr(module, "router", None)
        if router is not None:
            routers.append(router)
    return routers


all_routers: list[APIRouter] = _collect_routers()

__all__: Sequence[str] = ["all_routers"]
