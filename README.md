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

All commands are defined as UV scripts in `pyproject.toml` instead of using legacy approaches.

### Core Commands

```bash
# Workspace management
uv run dev-setup           # Complete environment setup
uv run install             # Install dependencies
uv run workspace-sync      # Sync all workspace dependencies
uv run workspace-update    # Update dependencies  
uv run workspace-tree      # Show dependency tree

# Code quality (using Ruff - faster than black+isort+flake8)
uv run format              # Format code
uv run format-check        # Check if code is formatted correctly
uv run lint                # Lint code
uv run lint-fix            # Auto-fix linting issues
uv run type-check          # Type checking with mypy
uv run quality             # Run all quality checks (format + lint + type-check)
uv run quality-check       # Check code quality without modifying files

# Testing
uv run test                # Run all tests
uv run test-verbose        # Run tests with verbose output

# Service development
uv run start-game-logic         # Start game-logic service (port 8000)
uv run start-player-management  # Start player-management service (port 8001)
uv run start-matchmaking        # Start matchmaking service (port 8002) 
uv run start-game-history       # Start game-history service (port 8003)

# Docker operations
uv run docker-build       # Build all Docker images
uv run docker-up          # Start all services with Docker Compose
uv run docker-down        # Stop all services
uv run docker-logs        # Show logs from all services
uv run docker-restart     # Restart all services

# Utilities
uv run clean               # Clean up build artifacts
```

### Alternative: Direct UV Commands

For power users who prefer direct commands:

```bash
# Quality checks
uv run ruff format .       # Format code
uv run ruff check .        # Lint code
uv run mypy .             # Type checking

# Testing
uv run pytest            # Run all tests

# Individual service testing
cd services/game-logic && uv run pytest  # Test specific service
```

### Windows PowerShell Support

All UV script commands work identically on Windows PowerShell:

```powershell
# Same commands work on Windows
uv run quality
uv run test
uv run start-matchmaking
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

1. **Setup environment**: `uv run dev-setup`
2. **Start services**: `uv run docker-up` or individual service commands
3. **Test the API**: Visit `http://localhost:8002/docs` for interactive API docs
4. **Play a game**: `POST http://localhost:8002/play` with `{"player": 1}`

## Development Workflow

1. Each service can be developed independently
2. Use `uv run quality` before committing
3. Services have their own test suites
4. Integration tests can be run from the root with `uv run test`
5. Each service has its own `pyproject.toml` for dependencies
6. Shared models are available via `from shared.models import ...`

