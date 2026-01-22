from pathlib import Path

#Root directory of project on local system
ROOT_DIRECTORY = Path(__file__).resolve().parents[1]

#Dictionary keys to be kept in the first step of cleaning. All other keys are 'obsolete' and will be deleted.
#Some keys contain information obtainable from kept keys (e.g. season from first four digits of game_id)
#Others contain information not planned to be used in the model (e.g. startTimeUTC)
KEEP_PBP = ["id", "gameDate", "awayTeam", "homeTeam", "gameOutcome", "plays", "rosterSpots"]
KEEP_TEAM = ["id", "abbrev"]

#Some keys in the cleaned play-by-data are dependent on event type.
#For example, oppPlayer comes from goalieId for goals, but playerId of winnign player for faceoffs
#Key that should be analyzed for the details key of our cleaned dictionary (by typeCode)
DETAIL_KEYS = {
    505: "shotType",
    506: "shotType",
    507: "shotType",
    508: "reason",
    509: "typeCode"
}

MAIN_PLAYER_KEYS = {
    502: "winningPlayerId",
    503: "hittingPlayerId",
    504: "playerId",
    505: "scoringPlayerId",
    506: "shootingPlayerId",
    507: "shootingPlayerId",
    508: "shootingPlayerId",
    509: "comittedByPlayerId",
    525: "playerId"
}

OPP_PLAYER_KEYS = {
    502: "losingPlayerId",
    503: "hitteePlayerId",
    505: "goalieInNetId",
    506: "goalieInNetId",
    507: "goalieInNetId",
    508: "blockingPlayerId",
    509: "drawnByPlayerId"
}
