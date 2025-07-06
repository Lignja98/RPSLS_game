"""FastAPI application entry-point.

The object `app` is imported by the ASGI server (Uvicorn) as

    uvicorn services.game.app.main:app
"""

from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.db.database import engine  # ensure engine is created at import time
from app.api.v1.endpoints import all_routers

# Initialise logging *before* anything else creates loggers
from app.core.logging import init_logging

init_logging()

# ---------------------------------------------------------------------------
# Middleware – request correlation ID
# ---------------------------------------------------------------------------
from app.core.middleware import request_id_middleware


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    """Application lifespan: dispose DB engine on shutdown."""

    yield  # startup – nothing special for now
    await engine.dispose()


settings = get_settings()

app = FastAPI(title=settings.APP_NAME, lifespan=lifespan)

# ---------------------------------------------------------------------------
# API routers
# ---------------------------------------------------------------------------
for r in all_routers:
    app.include_router(r, prefix=settings.API_V1_STR)

# Routers will be added as the implementation progresses
# from .api.v1.endpoints.health import router as health_router
# app.include_router(health_router, tags=["health"])

# ---------------------------------------------------------------------------
# CORS
# ---------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Middleware – request correlation ID
# ---------------------------------------------------------------------------
app.middleware("http")(request_id_middleware)

# ---------------------------------------------------------------------------
# Metrics – Prometheus (/metrics)
# ---------------------------------------------------------------------------
from prometheus_fastapi_instrumentator import Instrumentator

# Expose default FastAPI metrics without adding them to the OpenAPI schema.
Instrumentator().instrument(app).expose(app, include_in_schema=False)
