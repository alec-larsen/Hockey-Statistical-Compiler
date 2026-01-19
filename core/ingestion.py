import json

#import pandas as pd

import requests
from core import constants
from core.settings import CONNECTION_SUCCESS_MESSAGE

def write_play_by_play(game_id: int, loud: bool = CONNECTION_SUCCESS_MESSAGE) -> None:
    """
    Pull play-by-play data from NHL API and write data to local JSON file.

    Args:
        game_id (int): id of game to pull play-by-play of
    """
    try:
        pbp = requests.get(f"https://api-web.nhle.com/v1/gamecenter/{game_id}/play-by-play", timeout=10)
        if pbp.status_code != 200:
            raise ConnectionError(f"\033[91mCall to NHL API should yield status code 200, obtained status code {pbp.status_code} instead.\033[0m") # pylint: disable=line-too-long
        pbp_json = pbp.json()
    except TimeoutError as exc:
        raise TimeoutError("\033[91mResponse not received for API call. Please check connection.\033[0m") from exc

    if loud:
        print(f"\033[92mPull of play-by-play for game {game_id} successful!\033[0m")

    with open(constants.ROOT_DIRECTORY / "data" / "play-by-play" /f"{game_id}.json", mode = "w", encoding="utf-8") as file:
        json.dump(pbp_json, file, indent=2)
