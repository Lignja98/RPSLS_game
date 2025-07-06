from __future__ import annotations

"""Health-check endpoint."""

from fastapi import APIRouter, status

router = APIRouter()


@router.get("/healthz", status_code=status.HTTP_200_OK, summary="Liveness probe")
async def healthcheck() -> dict[str, str]:
    """Return 200 so orchestrators know the service is alive."""

    return {"status": "ok"}
