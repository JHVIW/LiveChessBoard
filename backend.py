from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import json

# Initialiseer de FastAPI applicatie
app = FastAPI()

# CORS middleware configuratie om cross-origin verzoeken toe te staan
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],           # Sta alle origin's toe
    allow_credentials=True,        # Sta het gebruik van credentials toe
    allow_methods=["*"],           # Sta alle HTTP-methoden toe
    allow_headers=["*"],           # Sta alle headers toe
)

# Configuratie voor de directory waar de schaakspellen worden opgeslagen
GAMES_DIR = Path("chess_games")
GAMES_DIR.mkdir(exist_ok=True)    # Maak de directory aan indien deze nog niet bestaat

@app.get("/game/{game_id}/current")
async def get_current_position(game_id: str):
    """
    Haal de huidige positie van een specifiek schaakspel op.

    Parameters:
    - game_id (str): De unieke identifier van het schaakspel.

    Returns:
    - dict: Bevat de FEN-string van de huidige positie, de status van het spel,
            de lengte van de geschiedenis en de timestamp van de laatste zet.

    Raises:
    - HTTPException 404: Indien het spel of de spelgegevens niet gevonden worden.
    """
    game_dir = GAMES_DIR / game_id
    if not game_dir.exists():
        raise HTTPException(status_code=404, detail="Game not found")
    
    moves_file = game_dir / "moves.json"
    if not moves_file.exists():
        raise HTTPException(status_code=404, detail="Game data not found")
    
    with open(moves_file) as f:
        moves = json.load(f)
    
    is_completed = (game_dir / "completed").exists()
    
    return {
        "fen": moves[-1]["fen"],
        "is_active": not is_completed,
        "history_length": len(moves),
        "timestamp": moves[-1]["timestamp"]
    }

@app.get("/game/{game_id}/history/{move_number}")
async def get_historical_position(game_id: str, move_number: int):
    """
    Haal de positie op van een specifiek zetnummer in een schaakspel.

    Parameters:
    - game_id (str): De unieke identifier van het schaakspel.
    - move_number (int): Het nulgebaseerde zetnummer waarvan de positie wordt opgehaald.

    Returns:
    - dict: Bevat de FEN-string van de positie, het zetnummer en de timestamp van die zet.

    Raises:
    - HTTPException 404: Indien het spel of de spelgegevens niet gevonden worden.
    - HTTPException 400: Indien het zetnummer ongeldig is.
    """
    game_dir = GAMES_DIR / game_id
    if not game_dir.exists():
        raise HTTPException(status_code=404, detail="Game not found")
    
    moves_file = game_dir / "moves.json"
    if not moves_file.exists():
        raise HTTPException(status_code=404, detail="Game data not found")
    
    with open(moves_file) as f:
        moves = json.load(f)
    
    if move_number < 0 or move_number >= len(moves):
        raise HTTPException(status_code=400, detail="Invalid move number")
    
    return {
        "fen": moves[move_number]["fen"],
        "move_number": move_number,
        "timestamp": moves[move_number]["timestamp"]
    }

@app.get("/game/{game_id}/moves")
async def get_moves(game_id: str):
    """
    Haal alle zetten op van een specifiek schaakspel en de actieve status.

    Parameters:
    - game_id (str): De unieke identifier van het schaakspel.

    Returns:
    - dict: Bevat een lijst van alle zetten en de actieve status van het spel.

    Raises:
    - HTTPException 404: Indien het spel of de spelgegevens niet gevonden worden.
    """
    game_dir = GAMES_DIR / game_id
    if not game_dir.exists():
        raise HTTPException(status_code=404, detail="Game not found")
    
    moves_file = game_dir / "moves.json"
    if not moves_file.exists():
        raise HTTPException(status_code=404, detail="Game data not found")
    
    with open(moves_file) as f:
        moves = json.load(f)
    
    is_completed = (game_dir / "completed").exists()
    
    return {
        "moves": moves,
        "is_active": not is_completed
    }
        
if __name__ == "__main__":
    import uvicorn
    # Start de applicatie met Uvicorn server op host 0.0.0.0 en poort 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)
