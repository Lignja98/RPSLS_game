"""FastAPI application entry-point.

The object `app` is imported by the ASGI server (Uvicorn) as

    uvicorn services.game.app.main:app
"""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI

from app.core.config import get_settings
from app.db.database import engine  # ensure engine is created at import time


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    """Application lifespan: dispose DB engine on shutdown."""

    yield  # startup – nothing special for now
    await engine.dispose()


settings = get_settings()

app = FastAPI(title=settings.APP_NAME, lifespan=lifespan)

# Routers will be added as the implementation progresses
# from .api.v1.endpoints.health import router as health_router
# app.include_router(health_router, tags=["health"])
