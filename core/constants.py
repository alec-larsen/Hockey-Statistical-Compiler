from pathlib import Path

#Root directory of project on local system
ROOT_DIRECTORY = Path(__file__).resolve().parents[1]

#Dictionary keys to be kept in the first step of cleaning. All other keys are 'obsolete' and will be deleted.
#Some keys contain information obtainable from kept keys (e.g. season from first four digits of game_id)
#Others contain information not planned to be used in the model (e.g. startTimeUTC)
KEEP_PBP = ["id", "gameDate", "awayTeam", "homeTeam", "gameOutcome", "plays", "rosterSpots"]
KEEP_TEAM = ["id", "abbrev"]
