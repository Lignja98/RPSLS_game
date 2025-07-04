# syntax=docker/dockerfile:1.4

# ---------- Base image ----------
FROM python:3.12-slim-bookworm AS base

ENV PYTHONUNBUFFERED=1 \
    # Prevents Python from writing .pyc files to disk
    PYTHONDONTWRITEBYTECODE=1

# ---------- Builder stage ----------
FROM base AS builder

# Copy the static uv binary (fast dependency installer/manager)
COPY --from=ghcr.io/astral-sh/uv:0.4.9 /uv /bin/uv

# Speed up installs & produce deterministic builds
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

WORKDIR /app

# 1. Copy only dependency manifests first to leverage Docker cache
#    If a uv.lock file is present it'll be copied alongside pyproject.toml
COPY pyproject.toml uv.lock* ./

# 2. Install dependencies (but not the project code) – uses Docker cache when deps unchanged
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev

# 3. Copy the actual application source
COPY . .

# 4. Install the project itself into an in-tree virtualenv (no dev deps)
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# ---------- Final runtime image ----------
FROM base

# Copy the installed virtualenv & source code from the builder image
COPY --from=builder /app /app

# Ensure the virtualenv's bin directory is on PATH
ENV PATH="/app/.venv/bin:$PATH"

WORKDIR /app

EXPOSE 8000

# NOTE: adjust the import path if your FastAPI instance lives elsewhere.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"] 