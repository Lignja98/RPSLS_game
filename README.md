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

## 🚀 Getting Started

### Prerequisites
- Python 3.12+
- UV package manager (`python -m pip install uv`)
- Docker (optional, for containerized deployment)
- Git

### Quick Setup

```bash
# Clone and enter the repository
git clone <repository-url>
cd RPSLS_game

# Install dependencies
uv sync --all-packages

# Start all services (choose one option):
docker compose up     # Option A: Using Docker
# OR
uvicorn services.matchmaking.app.main:app --reload --port 8002  # Option B: Development mode
```

Visit `http://localhost:8002/docs` for interactive API documentation.

### Running Individual Services

```bash
# Game Logic Service (Port 8000)
cd services/game_logic && uvicorn app.main:app --reload --port 8000

# Player Management Service (Port 8001)
cd services/player_management && uvicorn app.main:app --reload --port 8001

# Matchmaking Service (Port 8002)
cd services/matchmaking && uvicorn app.main:app --reload --port 8002

# Game History Service (Port 8003)
cd services/game_history && uvicorn app.main:app --reload --port 8003
```

## 💻 Development Guide

### Code Quality Tools
```bash
# Formatting and Linting
ruff format .        # Format code
ruff check .         # Lint code
mypy .              # Type checking

# Testing
pytest              # Run all tests
pytest -v           # Verbose output
pytest services/game_logic/tests  # Test specific service

# Cleanup
find . -type d -name "__pycache__" -exec rm -r {} +
find . -type d -name ".pytest_cache" -exec rm -r {} +
find . -type d -name ".ruff_cache" -exec rm -r {} +
find . -type d -name ".mypy_cache" -exec rm -r {} +
```

### Docker Operations
```bash
docker compose up --build  # Build and start all services
docker compose down       # Stop services
docker compose logs -f    # View logs
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
│   ├── game_logic/     # Stateless game rules
│   ├── player_management/  # Player data & stats
│   ├── matchmaking/    # Game orchestration
│   └── game_history/   # Game logging
├── shared/             # Common models & utilities
├── pyproject.toml      # UV workspace + scripts configuration
└── docker-compose.yml  # Development orchestration
```

## External Dependencies

- **Random Number API**: `https://codechallenge.boohma.com/random`
  - Returns random number 1-100 for computer choice generation

