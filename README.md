# RPSLS Game - Microservices Architecture

> A production-ready Rock Paper Scissors Lizard Spock game built with Python microservices, demonstrating modern software architecture patterns and development practices.

## 🌟 Highlights

- **🏗️ Microservices Architecture** - 4 independent services with clear separation of concerns
- **⚡ Modern Python Tooling** - UV workspace + Ruff for 10x faster development
- **🔧 Production Ready** - Docker, PostgreSQL, async APIs, comprehensive testing
- **🚀 Developer Friendly** - Hot reload, type checking, automated formatting

## 🎮 What It Does

This is an advanced implementation of the classic "Rock Paper Scissors Lizard Spock" game (made famous by The Big Bang Theory). Instead of a simple script, it's built as a distributed system with independent services that communicate via REST APIs.

**Game Rules:** Scissors cuts Paper covers Rock crushes Lizard poisons Spock smashes Scissors decapitates Lizard eats Paper disproves Spock vaporizes Rock crushes Scissors.

## Architecture Overview

This project implements a distributed microservices architecture with the following services:

### Services

| Service | Port | Responsibility | Dependencies |
|---------|------|----------------|--------------|
| **Game Logic** | 8000 | Stateless game rules engine | FastAPI, Pydantic |
| **Player Management** | 8001 | Player CRUD & statistics | FastAPI, SQLAlchemy, PostgreSQL |
| **Matchmaking** | 8002 | Game orchestration & coordination | FastAPI, httpx |
| **Game History** | 8003 | Game logging & retrieval | FastAPI, SQLAlchemy, PostgreSQL |

## 🚀 Quick Start

**Prerequisites:** Python 3.12+ and UV package manager

```bash
# 1. Clone and setup
git clone <repository>
cd RPSLS_game

# 2. One command setup (installs everything)
uv run dev-setup

# 3. Start the game (choose one):

# Option A: All services with Docker
uv run docker-up

# Option B: Individual services for development
uv run start-matchmaking
# Then visit http://localhost:8002/docs to play!
```

**🎯 Play the game:** Visit `http://localhost:8002/docs` and use the `/play` endpoint with `{"player": 1}` (1=rock, 2=paper, 3=scissors, 4=lizard, 5=spock)

## Development Setup

### Prerequisites

- Python 3.12+
- UV package manager ([install here](https://docs.astral.sh/uv/getting-started/installation/))
- Docker & Docker Compose (optional)

### Full Development Setup

```bash
# Setup UV workspace (installs all services + shared dependencies)
uv run dev-setup

# Start all services individually for development
uv run start-game-logic      # Port 8000
uv run start-player-management   # Port 8001  
uv run start-matchmaking     # Port 8002
uv run start-game-history    # Port 8003
```

## UV Workspace Benefits

This project uses **UV workspace** for optimal dependency management:

- ✅ **Shared dependencies** - Common packages cached once
- ✅ **Local package references** - Services can `import shared.models`
- ✅ **Independent services** - Each has its own `pyproject.toml`
- ✅ **Fast installs** - Workspace-aware dependency resolution

## Development Commands

The project uses direct commands for development operations. Here are the key commands you'll need:

### Core Commands

```bash
# Development Setup
python -m pip install uv  # Install UV if you haven't already
uv pip install -e .      # Install the project in editable mode

# Service Development (using uvicorn directly)
uvicorn services.game_logic.app.main:app --reload --port 8000         # Start game-logic service
uvicorn services.player_management.app.main:app --reload --port 8001  # Start player-management service
uvicorn services.matchmaking.app.main:app --reload --port 8002        # Start matchmaking service
uvicorn services.game_history.app.main:app --reload --port 8003       # Start game-history service

# Code Quality
ruff format .            # Format code
ruff check .            # Lint code
mypy .                  # Type checking

# Testing
pytest                  # Run all tests
pytest -v               # Run tests with verbose output
pytest services/game-logic/tests  # Test specific service

# Docker Operations
docker compose build    # Build all services
docker compose up       # Start all services
docker compose down     # Stop all services
docker compose logs     # View service logs
docker compose restart  # Restart services

# Cleanup
find . -type d -name "__pycache__" -exec rm -r {} +  # Clean Python cache
find . -type d -name ".pytest_cache" -exec rm -r {} +  # Clean pytest cache
find . -type d -name ".ruff_cache" -exec rm -r {} +    # Clean ruff cache
find . -type d -name ".mypy_cache" -exec rm -r {} +    # Clean mypy cache
```

### Windows PowerShell Support

The same commands work on Windows PowerShell with slight modifications:

```powershell
# Development
uvicorn services.game_logic.app.main:app --reload --port 8000

# Quality & Testing
ruff format .
pytest

# Docker
docker compose up
```

## API Endpoints

### Game Service (Port 8002 - Matchmaking)

The main game endpoints that match the requirements:

- `GET /choices` - Get all available choices (1-5: rock, paper, scissors, lizard, spock)
- `GET /choice` - Get a random computer choice
- `POST /play` - Play a game round
  ```json
  {
    "player": 1  // Choice ID (1-5)
  }
  ```

### Individual Services

Each service exposes its own API:

- **Game Logic (8000)**: `/evaluate` - Determine winner given two choices
- **Player Management (8001)**: `/players` - CRUD operations
- **Game History (8003)**: `/games` - Game history retrieval

## Service Communication

Services communicate via REST APIs:

1. **Matchmaking** receives game requests
2. Validates player via **Player Management**
3. Gets computer choice using external random API
4. Evaluates winner via **Game Logic**
5. Logs game via **Game History**
6. Updates player stats via **Player Management**

## Technology Stack

- **Runtime**: Python 3.12, FastAPI, Uvicorn
- **Package Management**: UV with workspace support
- **Database**: PostgreSQL with async SQLAlchemy
- **HTTP Client**: httpx for inter-service communication
- **Containerization**: Docker & Docker Compose
- **Testing**: pytest with async support
- **Code Quality**: Ruff, mypy
- **Configuration**: Pure pyproject.toml approach

## Project Structure

```
RPSLS_game/
├── services/           # Individual microservices
│   ├── game-logic/     # Stateless game rules
│   ├── player-management/  # Player data & stats
│   ├── matchmaking/    # Game orchestration
│   └── game-history/   # Game logging
├── shared/             # Common models & utilities
├── pyproject.toml      # UV workspace + scripts configuration
└── docker-compose.yml  # Development orchestration
```

## External Dependencies

- **Random Number API**: `https://codechallenge.boohma.com/random`
  - Returns random number 1-100 for computer choice generation

## Getting Started

1. **Setup environment**:
   ```bash
   # Install UV if you haven't already
   python -m pip install uv
   
   # Install project dependencies
   uv pip install -e .
   ```

2. **Start services**: 
   ```bash
   # Option A: Using Docker (recommended for first-time setup)
   docker compose up
   
   # Option B: Individual services for development
   uvicorn services.matchmaking.app.main:app --reload --port 8002
   ```

3. **Test the API**: Visit `http://localhost:8002/docs` for interactive API docs
4. **Play a game**: Use the Swagger UI or send a POST request:
   ```bash
   curl -X POST http://localhost:8002/play -H "Content-Type: application/json" -d '{"player": 1}'
   ```

## Development Workflow

1. **Service Independence**: Each service can be developed independently in its own directory under `services/`

2. **Code Quality**: Before committing changes:
   ```bash
   # Format and lint code
   ruff format .
   ruff check .
   
   # Run type checking
   mypy .
   ```

3. **Testing**: 
   ```bash
   # Run all tests
   pytest
   
   # Test specific service
   pytest services/game-logic/tests
   ```

4. **Dependencies**: 
   - Each service has its own `pyproject.toml` for service-specific dependencies
   - Shared dependencies are managed in the root `pyproject.toml`
   - Use `from shared.models import ...` to access common code

5. **Local Development**:
   - Use `--reload` flag with uvicorn for auto-reloading during development
   - Run dependent services with Docker while developing a specific service
   - Use the Swagger UI at `/docs` to test your endpoints

