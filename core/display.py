from core.constants import BANNER_LENGTH

def get_menu_option():
    return input("Please choose one of the following functionalities to execute:\n"
      + "1. Ingestion pass: Ingest 100 play-by-plays from the NHL API\n"
      + "2. Cleaning pass: Clean all previously ingested raw data.\n"
      + "3. Exit.\n")

def print_banner(message: str):
    print("-"*BANNER_LENGTH + "\n" + message + "\n" + "-" * BANNER_LENGTH)

def banner(message: str) -> str:
    return "-"*BANNER_LENGTH + "\n" + message + "\n" + "-" * BANNER_LENGTH

def missing_games_message(game_ids: list[int]) -> str:
    """
    Format message describing all games with no raw play-by-play data on local system.

    Args:
        game_ids (list[int]): List of all game_ids found to be missing in data/raw/
        
    Returns:
        str: Formatted string to be printed from verify_raw_data.
    """
    message = f"All required raw game data expected to be found, but {len(game_ids)} games are missing data.\n"

    message += banner("MISSING GAME IDS") + "\n"

    for i in range(min(len(game_ids),10)):
        message += f"{game_ids[i]}\n"

    if len(game_ids) > 10:
        message += f"and {len(game_ids)-10} more not listed"

    return message
