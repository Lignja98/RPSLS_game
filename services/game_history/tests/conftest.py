import asyncio
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from datetime import datetime, UTC
from services.game_history.app.database import Base
from services.game_history.app.models import GameHistory
from shared.models import Choice, GameResult

# Test database URL - using SQLite for tests
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
async def test_engine():
    """Create a test database engine."""
    engine = create_async_engine(
        TEST_DATABASE_URL,
        echo=False,
        future=True,
        connect_args={"check_same_thread": False}  # Allow SQLite to be used with multiple threads
    )
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield engine
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    
    await engine.dispose()

@pytest.fixture(scope="module")
async def test_session(test_engine):
    """Create a test database session."""
    TestSessionLocal = sessionmaker(
        test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False
    )
    
    async with TestSessionLocal() as session:
        yield session
        await session.rollback()  # Ensure clean state between tests

@pytest.fixture(scope="function")
async def sample_game_history(test_session):
    """Create a sample game history record for testing."""
    game = GameHistory(
        player_id=1,
        player_choice=Choice.ROCK,
        computer_choice=Choice.SCISSORS,
        result=GameResult.WIN,
        winning_move="Rock crushes Scissors",
        played_at=datetime.now(UTC)
    )
    
    test_session.add(game)
    await test_session.commit()
    await test_session.refresh(game)
    
    yield game
    
    # Clean up
    await test_session.delete(game)
    await test_session.commit()
    # No need to refresh after deletion; the instance is gone from the session 