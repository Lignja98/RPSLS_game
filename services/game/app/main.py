"""FastAPI application entrypoint for the RPSLS game service."""

from fastapi import FastAPI

app = FastAPI(title="RPSLS Game Service")

# Routers will be added as the implementation progresses
# from .api.v1.endpoints.health import router as health_router
# app.include_router(health_router, tags=["health"]) 