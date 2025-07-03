import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from services.game_history.app.main import app
from services.game_history.app.database import get_db_session
from services.game_history.app.models import GameHistory
from shared.models import Choice, GameResult

# Global test session for sharing across tests
test_session_global = None

def override_get_db():
    """Override the database dependency for testing."""
    return test_session_global

@pytest.fixture(scope="module", autouse=True)
def test_client(test_session):
    """Create a test client with the test database session."""
    global test_session_global
    test_session_global = test_session
    app.dependency_overrides[get_db_session] = override_get_db
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()
    test_session_global = None

@pytest.mark.asyncio
async def test_create_game_history(test_client):
    """Test creating a new game history record via API."""
    game_data = {
        "player_id": 1,
        "player_choice": Choice.ROCK.value,
        "computer_choice": Choice.SCISSORS.value,
        "result": GameResult.WIN.value,
        "winning_move": "Rock crushes Scissors"
    }
    
    response = test_client.post("/games", json=game_data)
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "id" in data
    assert isinstance(data["id"], int)

@pytest.mark.asyncio
async def test_get_game_history(test_client, sample_game_history):
    """Test retrieving a game history record via API."""
    response = test_client.get(f"/games/{sample_game_history.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == sample_game_history.id
    assert data["player_id"] == sample_game_history.player_id
    assert data["player_choice"] == sample_game_history.player_choice.value
    assert data["result"] == sample_game_history.result.value

@pytest.mark.asyncio
async def test_get_nonexistent_game(test_client):
    """Test retrieving a non-existent game via API."""
    response = test_client.get("/games/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Game not found"

@pytest.mark.asyncio
async def test_list_games(test_client, sample_game_history):
    """Test listing games via API with various filters."""
    # Test without filters
    response = test_client.get("/games")
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "entries" in data
    assert len(data["entries"]) > 0
    
    # Test with player filter
    response = test_client.get(f"/games?player_id={sample_game_history.player_id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data["entries"]) > 0
    assert all(g["player_id"] == sample_game_history.player_id for g in data["entries"])
    
    # Test with result filter
    response = test_client.get(f"/games?result={sample_game_history.result.value}")
    assert response.status_code == 200
    data = response.json()
    assert len(data["entries"]) > 0
    assert all(g["result"] == sample_game_history.result.value for g in data["entries"])

@pytest.mark.asyncio
async def test_get_player_statistics(test_client, sample_game_history):
    """Test retrieving player statistics via API."""
    response = test_client.get(f"/players/{sample_game_history.player_id}/stats")
    assert response.status_code == 200
    data = response.json()
    assert "player_id" in data
    assert "stats" in data
    assert isinstance(data["stats"], dict)
    assert all(isinstance(count, int) for count in data["stats"].values())

@pytest.mark.asyncio
async def test_cleanup_old_records(test_client):
    """Test cleaning up old records via API."""
    response = test_client.delete("/games/cleanup", params={"days": 30})
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "deleted_count" in data
    assert isinstance(data["deleted_count"], int) 