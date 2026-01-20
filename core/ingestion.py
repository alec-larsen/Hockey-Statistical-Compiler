import json
import datetime

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

def gtd(today: datetime.date = datetime.date.today(), loud: bool = CONNECTION_SUCCESS_MESSAGE) -> int:
    """
    Find number of games up to, but not including today.

    Returns:
        int: Number of games that have occurred so far in the NHL regular season.
    """
    yesterday = str(today - datetime.timedelta(days=1))

    try:
        sched = requests.get(f"https://api-web.nhle.com/v1/schedule/{yesterday}", timeout=10)
        if sched.status_code != 200:
            raise ConnectionError(f"\033[91mCall to NHL API should yield status code 200, obtained status code {sched.status_code} instead.\033[0m") # pylint: disable=line-too-long
        sched_json = sched.json() #This gives us a dictionary of the week of games containing yesterday.
    except TimeoutError as exc:
        raise TimeoutError("\033[91mResponse not received for API call. Please check connection.\033[0m") from exc

    if loud:
        print("\033[92mPull of schedule to date for current season successful!\033[0m")

    #Obtain only yesterday's game data.
    #List comprehension generates a list with one element, so we take [0] to access it.
    day = [d for d in sched_json["gameWeek"] if d["date"] == yesterday][0]

    #Since last four digits of game_id represent regular season order, so largest game_id is most recent game.
    #Find maximum game_id in yesterday's game data
    max_game_id = max([game["id"] for game in day["games"]])

    #Last four digits of maximum game_id yield number of games that have happened so far in the regular season.
    return max_game_id % 10000
