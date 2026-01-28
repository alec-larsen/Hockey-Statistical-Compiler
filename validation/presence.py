#Validation functions check for presence of all files required for certain model operations.
import os

from validation.verification_error import VerificationError
from core.constants import ROOT_DIRECTORY
from core.ingestion import PBP_CODES
from core.display import missing_games_message

def verify_raw_data():
    """
    Check for presence of all required raw play-by-play data.
    """
    #Get list of all game_ids with play-by-play data in data/raw/
    game_ids = [int(f[:-5]) for f in os.listdir(ROOT_DIRECTORY / "data" / "raw") if f != ".gitkeep"]

    unadded_games: list[int] = []

    for code in PBP_CODES:
        if code not in game_ids:
            unadded_games.append(code)

    if not unadded_games:
        raise VerificationError(missing_games_message(unadded_games))

    else:
        print("\033[92mRAW DATA CHECK PASSED: ALL RAW DATA PRESENT ON SYSTEM\033[0m")
