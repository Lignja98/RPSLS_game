# RPSLS Game – Single-Service Edition

A **FastAPI** micro-service that plays *Rock Paper Scissors Lizard Spock*, stores each game in PostgreSQL, and exposes a simple REST API you can paste into the provided UI.

---

## 📂 Project Layout

```
RPSLS_game/
├── services/
│   └── game/            # FastAPI application code & tests
│       ├── app/
│       ├── tests/
│       └── Dockerfile   # multi-stage, uv-powered image
├── pyproject.toml       # dependencies, linting, test config
├── docker-compose.yml   # game service + Postgres
└── README.md
```

---

## 🚀 Quick Start (recommended)

> Requires Docker + Docker Compose only

```bash
# 1. Clone
$ git clone <repo> && cd RPSLS_game

# 2. Build & run everything
$ docker compose up --build -d

# 3. Play!
Open http://localhost:8000/docs          # Swagger UI
```

The Compose file launches:

| Service | Port | Purpose |
|---------|------|---------|
| game    | 8000 | FastAPI app running under Uvicorn |
| postgres| 5432 | Persistent store for game history |

Health-checks make the game service wait for Postgres before starting.

---

## 🛠️ Local Development

If you prefer editing outside Docker:

```bash
# Install uv once
python -m pip install --upgrade uv

# Create a virtual-env and install deps (including dev tools)
uv sync

# Set your DB URL (or start Postgres via Docker)
export DATABASE_URL="postgresql+asyncpg://rpsls_user:rpsls_password@localhost:5432/rpsls_db"

# Run the API with hot-reload
uv run uvicorn services.game.app.main:app --reload
```

### Useful commands
```bash
ruff format .      # auto-format
ruff check .       # lint
mypy .             # type-check
pytest             # run tests
```

---

## 📑 API Overview (to be implemented)

| Method | Path            | Description |
|--------|-----------------|-------------|
| GET    | /health         | Liveness probe |
| GET    | /choices        | List available moves |
| POST   | /play           | Play a round – returns winner |
| GET    | /history        | Paginated list of past games |
| GET    | /players/{id}   | Aggregated statistics |

(OpenAPI docs are auto-generated at `/docs`.)

---

## ⚙️ Tech Stack

* Python 3.12
* FastAPI  
* SQLAlchemy 2.0 (async) + Alembic migrations  
* Pydantic v2 models
* **uv** for dependency management & deterministic builds
* Ruff, MyPy, Pytest for code quality
* Docker multi-stage image

---

### Made with ❤️ – enjoy reviewing!

