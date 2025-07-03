from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from shared.models import Choice, ChoiceResponse

from .game import GameLogic, GameOutcome, GameRound

# Create FastAPI app
app = FastAPI(
    title="RPSLS Game Logic Service",
    description="Game logic microservice for Rock Paper Scissors Lizard Spock",
    version="1.0.0",
)


@app.get("/health")
async def health_check() -> JSONResponse:
    """Health check endpoint."""
    return JSONResponse({"status": "healthy"})


@app.get("/choices")
async def get_choices() -> dict[str, list[ChoiceResponse]]:
    """Get all valid choices for the game.

    Returns:
        dict: Dictionary containing list of valid choices with their IDs and names
    """
    # Map enum values to 1-5 for API compatibility
    choice_to_id = {
        Choice.ROCK: 1,
        Choice.PAPER: 2,
        Choice.SCISSORS: 3,
        Choice.LIZARD: 4,
        Choice.SPOCK: 5
    }
    
    choices = [
        ChoiceResponse(id=choice_to_id[choice], name=choice)
        for choice in GameLogic.get_valid_moves()
    ]
    return {"choices": choices}


@app.post("/evaluate", response_model=GameOutcome)
async def evaluate_game(game_round: GameRound) -> GameOutcome:
    """Evaluate a game round and determine the winner.

    Args:
        game_round (GameRound): The game round to evaluate

    Returns:
        GameOutcome: The result of the game round

    Raises:
        HTTPException: If invalid choices are provided
    """
    # Validate choices
    valid_moves = GameLogic.get_valid_moves()
    if (game_round.player_one_choice not in valid_moves or 
        game_round.player_two_choice not in valid_moves):
        raise HTTPException(
            status_code=400,
            detail="Invalid choice provided. Must be one of: rock, paper, scissors, lizard, spock"
        )

    # Evaluate the game round
    return GameLogic.evaluate_round(game_round) 