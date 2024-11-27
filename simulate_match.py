import chess
import random
import time
import json
import os
from pathlib import Path
from threading import Lock

class ChessSimulator:
    """
    Simuleert een schaakspel door willekeurige zetten te genereren en deze op te slaan.
    
    Deze klasse beheert het aanmaken van nieuwe spellen, het simuleren van zetten,
    en het opslaan van de spelgeschiedenis in JSON-bestanden.
    """
    
    def __init__(self, games_dir="chess_games"):
        """
        Initialiseer de ChessSimulator.
        
        Parameters:
        - games_dir (str): De directory waar schaakspellen worden opgeslagen. 
                           Standaard is dit "chess_games".
        """
        self.games_dir = Path(games_dir)
        self.games_dir.mkdir(exist_ok=True)  # Maak de directory aan indien deze nog niet bestaat
        self.file_lock = Lock()               # Lock voor thread-safe bestandstoegang

    def generate_game_id(self):
        """
        Genereer een unieke game ID en maak een bijbehorende directory aan.
        
        Returns:
        - game_id (str): Een unieke 6-cijferige game ID.
        """
        while True:
            # Genereer een willekeurige 6-cijferige ID
            game_id = ''.join(random.choices('0123456789', k=6))
            game_dir = self.games_dir / game_id
            if not game_dir.exists():
                game_dir.mkdir()
                return game_id

    def simulate_game(self, game_id, move_delay=2):
        """
        Simuleer een schaakspel en sla de zetten op in een JSON-bestand.
        
        Parameters:
        - game_id (str): De unieke identifier van het schaakspel.
        - move_delay (int): De vertraging in seconden tussen zetten. 
                            Standaard is dit 2 seconden.
        """
        game_dir = self.games_dir / game_id
        moves_file = game_dir / "moves.json"

        # Initialiseer het schaakbord en de lijst met zetten
        board = chess.Board()

        # Lees bestaande zetten indien aanwezig
        if moves_file.exists():
            with open(moves_file) as f:
                moves = json.load(f)
        else:
            # Voeg de startpositie toe aan de zettenlijst
            moves = [{"fen": board.fen(), "timestamp": time.time()}]
            self._save_moves(moves_file, moves)

        # Simuleer zetten totdat het spel is afgelopen
        while not board.is_game_over():
            time.sleep(move_delay)  # Wacht voor de volgende zet

            # Verkrijg alle legale zetten en evalueer ze
            legal_moves = list(board.legal_moves)
            scored_moves = []

            for move in legal_moves:
                score = 0
                # Prioriteer captures
                if board.is_capture(move):
                    score += 50
                # Stimuleer controle over het centrum
                to_square = move.to_square
                if to_square in [27, 28, 35, 36]:  # D4, E4, D5, E5
                    score += 20
                # Prioriteer zetten die schaak geven
                board.push(move)
                if board.is_check():
                    score += 30
                board.pop()

                # Voeg een willekeurige component toe aan de score
                scored_moves.append((move, score + random.randint(0, 10)))

            # Sorteer zetten op basis van score en selecteer een zet
            scored_moves.sort(key=lambda x: x[1], reverse=True)
            if len(scored_moves) == 1:
                selected_move = scored_moves[0][0]
            else:
                # Kies willekeurig tussen de top 4 zetten
                selected_move = scored_moves[random.randint(0, min(3, len(scored_moves)-1))][0]

            # Voer de geselecteerde zet uit
            board.push(selected_move)
            moves.append({
                "fen": board.fen(),
                "timestamp": time.time()
            })

            # Sla de zetten op na elke zet met thread-safe locking
            self._save_moves(moves_file, moves)

        # Markeer het spel als voltooid door een 'completed' bestand aan te maken
        with open(game_dir / "completed", "w") as f:
            f.write(str(time.time()))

    def _save_moves(self, moves_file, moves):
        """
        Sla de zetten op in een JSON-bestand op een thread-safe manier.
        
        Parameters:
        - moves_file (Path): Het pad naar het moves.json bestand.
        - moves (list): De lijst met zetten die moeten worden opgeslagen.
        """
        with self.file_lock:
            # Schrijf naar een tijdelijk bestand
            temp_file = moves_file.parent / f"{moves_file.name}.tmp"

            with open(temp_file, 'w') as f:
                json.dump(moves, f, indent=2)

            # Hernoem het tijdelijke bestand naar moves.json (atomische operatie)
            if moves_file.exists():
                moves_file.unlink()
            os.rename(temp_file, moves_file)

if __name__ == "__main__":
    # Initialiseer de simulator en start een nieuw spel
    simulator = ChessSimulator()
    game_id = simulator.generate_game_id()
    print(f"Starting new game with ID: {game_id}")
    simulator.simulate_game(game_id)
