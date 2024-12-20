# Chess Game API

## Overzicht

De **Chess Game API** is een RESTful API gebouwd met FastAPI voor het beheren en volgen van schaakspellen. Deze applicatie maakt het mogelijk om de huidige positie van een schaakspel op te vragen, historische posities te bekijken en de volledige zetgeschiedenis te raadplegen. Daarnaast bevat de applicatie een simulatiecomponent die automatisch willekeurige schaakzetten genereert en opslaat, waardoor het eenvoudig is om nieuwe spellen te starten en te volgen.

## Functies

- **Huidige Positie Opvragen:** Verkrijg de actuele FEN-string van een schaakspel, de status (actief of voltooid), de lengte van de zetgeschiedenis en de timestamp van de laatste zet.
- **Historische Positie Bekijken:** Haal de positie op van een specifiek zetnummer binnen een schaakspel, inclusief de FEN-string, het zetnummer en de timestamp.
- **Zetgeschiedenis Opvragen:** Bekijk alle zetten van een schaakspel en de huidige actieve status van het spel.
- **Spel Simulatie:** Automatisch genereren en uitvoeren van willekeurige schaakzetten met prioriteit voor captures, controle over het centrum en zetten die schaak geven.
- **Thread-safe Opslag:** Veilig opslaan van zetgeschiedenis in JSON-bestanden met behulp van threading locks.

## API Endpoints

### 1. Huidige Positie van een Spel
**Endpoint:** `/game/{game_id}/current`

**Beschrijving:** Haalt de huidige positie van een specifiek schaakspel op, inclusief de FEN-string, de status van het spel, de lengte van de geschiedenis en de timestamp van de laatste zet.

**Response:**
```json
{
  "fen": "FEN-string",
  "is_active": true,
  "history_length": 20,
  "timestamp": 1617181723.456
}
```

### 2. Historische Positie van een Zet
**Endpoint:** `/game/{game_id}/history/{move_number}`

**Beschrijving:** Haalt de positie op van een specifiek zetnummer in een schaakspel, inclusief de FEN-string, het zetnummer en de timestamp van die zet.

**Response:**
```json
{
  "fen": "FEN-string",
  "move_number": 10,
  "timestamp": 1617181723.456
}
```

### 3. Alle Zetten van een Spel
**Endpoint:** `/game/{game_id}/moves`

**Beschrijving:** Haalt alle zetten op van een specifiek schaakspel en geeft de actieve status van het spel terug.

**Response:**
```json
{
  "moves": [
    {
      "fen": "FEN-string",
      "timestamp": 1617181723.456
    },
    ...
  ],
  "is_active": true
}
```

## Chess Simulator

De `ChessSimulator` klasse simuleert een schaakspel door willekeurige zetten te genereren en deze op te slaan in JSON-bestanden. De simulator beheert het aanmaken van nieuwe spellen, het simuleren van zetten met een vertraging tussen elke zet, en het veilig opslaan van de spelgeschiedenis met behulp van thread-safe locking.

### Functionaliteiten:
- **Unieke Game ID:** Genereert een unieke 6-cijferige identifier voor elk nieuw spel.
- **Zet Simulatie:** Voert zetten uit op basis van een score-systeem dat captures, controle over het centrum en zetten die schaak geven prioriteert.
- **Geschiedenis Opslag:** Slaat elke zet op in een `moves.json` bestand binnen de game directory.
- **Spel Voltooiing:** Markeert het spel als voltooid door een `completed` bestand aan te maken zodra het spel is afgelopen.

## Bestandsstructuur

```
chess_games/
├── {game_id}/
│   ├── moves.json      # Bevat de lijst van zetten met FEN-strings en timestamps.
│   └── completed       # Een bestand dat de voltooiing van het spel aangeeft.
```

## Technologieën

- **FastAPI:** Voor het bouwen van de RESTful API.
- **Uvicorn:** ASGI server voor het draaien van de FastAPI applicatie.
- **Chess.py:** Voor het beheren van het schaakbord en zetten.
- **JSON:** Voor het opslaan van zetgeschiedenis.
- **Threading:** Voor veilige bestandsoperaties tijdens het simuleren van zetten.

---

Deze applicatie biedt een solide basis voor het beheren en simuleren van schaakspellen via een API, met mogelijkheden voor verdere integratie en uitbreiding.
