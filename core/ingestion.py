import json
from typing import Any
import datetime
import os
import requests

from core import constants
from validation.exceptions import ExcessDelayError, NetworkError

def clean_pbp(pbp_json: dict[str, Any]) -> dict[str, Any]:
    """
    Clean raw play-by-play data from NHL API into more concise format.

    Args:
        pbp_json (dict): Raw play-by-play data from NHL API, as Python dictionary.
    """
    #Keep only required keys, all others in raw data will not be used in the model.
    pbp_json = {k: pbp_json[k] for k in constants.KEEP_PBP}

    #Add margin of victory; positive for home win, negative for away win.
    pbp_json["margin"] = pbp_json["homeTeam"]["score"] - pbp_json["awayTeam"]["score"]

    #Reduce team desciptions to only keys listed in KEEP_TEAM.
    pbp_json["homeTeam"] = {k: pbp_json["homeTeam"][k] for k in constants.KEEP_TEAM}
    pbp_json["awayTeam"] = {k: pbp_json["awayTeam"][k] for k in constants.KEEP_TEAM}

    #Flatten gameOutcome; will be used to note whether game went to overtime or shootout
    pbp_json["gameOutcome"] = pbp_json["gameOutcome"]["lastPeriodType"]

    #Flatten rosterSpots; remove unneccesary keys
    pbp_json["rosterSpots"] = [{
        "teamId": player["teamId"],
        "playerId": player["playerId"],
        "name": player["firstName"]["default"] + " " + player["lastName"]["default"],
        "position": player["positionCode"]
    } for player in pbp_json["rosterSpots"]]

    #Get rid of period start and stoppage announcements
    pbp_json["plays"] = [play for play in pbp_json["plays"] if play["typeCode"] not in constants.REMOVED_PLAY_CODES]
    #Flatten remaining plays, leaving only vital information.
    pbp_json["plays"] = [{
        "eventId": play["eventId"],
        "type": play["typeCode"],
        "x": -play["details"]["xCoord"] if play["homeTeamDefendingSide"] == "Right" else play["details"]["xCoord"], #Modifed such that home team always shoots on positive x-coordinate net.
        "y": play["details"]["yCoord"],
        #Not every event type has/needs additional details. Assign all details of events without a specified details field to None
        "details": (play["details"][constants.DETAIL_KEYS[play["typeCode"]]] if constants.DETAIL_KEYS.get(play["typeCode"]) is not None and 
                    play["details"].get(constants.DETAIL_KEYS.get(play["typeCode"])) is not None else None),
        #Consolidate all fields involving main player in given play into one key.
        #Some plays may not have main players.
        #Bench minor penalties are not listed as committed by a single player (rather they're served by a specific player). We do not count these against said player.
        "mainPlayer": (play["details"][constants.MAIN_PLAYER_KEYS[play["typeCode"]]] if constants.MAIN_PLAYER_KEYS.get(play["typeCode"]) is not None and
                       play["details"].get(constants.MAIN_PLAYER_KEYS.get(play["typeCode"])) is not None else None),
        "mainTeam": play["details"]["eventOwnerTeamId"],
        #Not every event involves an opposing player. Assign oppPlayer of any event without an opposing player to None.
        #Note: some play types that usually have opposing players may not in certain situations (e.g. empty net goals have no listed goalie.)
        "oppPlayer": (play["details"][constants.OPP_PLAYER_KEYS[play["typeCode"]]] if constants.OPP_PLAYER_KEYS.get(play["typeCode"]) is not None and
                      play["details"].get(constants.OPP_PLAYER_KEYS.get(play["typeCode"])) is not None else None),
        "assist1": play["details"]["assist1PlayerId"] if play["typeCode"] == 505 and play["details"].get("assist1PlayerId") is not None else None,
        "assist2": play["details"]["assist2PlayerId"] if play["typeCode"] == 505 and play["details"].get("assist2PlayerId") is not None else None
    } for play in pbp_json["plays"]]

    return pbp_json

def gtd(today: datetime.date = datetime.date.today()) -> int:
    """
    Find number of games up to, but not including today.

    Returns:
        int: Number of games that have occurred so far in the NHL regular season.
    """
    yesterday = str(today - datetime.timedelta(days=1))

    try:
        sched = requests.get(f"https://api-web.nhle.com/v1/schedule/{yesterday}", timeout=10)
        if sched.status_code != 200:
            raise NetworkError(f"\033[91mCall to NHL API should yield status code 200, obtained status code {sched.status_code} instead.\033[0m")
        sched_json = sched.json() #This gives us a dictionary of the week of games containing yesterday.

    except requests.exceptions.ConnectionError as exc:
        raise NetworkError("\033[91mResponse unable to be received from API. Please check internet connection.\033[0m") from exc

    except requests.exceptions.Timeout as exc:
        raise ExcessDelayError("\033[91mResponse not received for API call within 10 seconds. Please check internet connection.\033[0m") from exc

    #Obtain only yesterday's game data.
    #List comprehension generates a list with one element, so we take [0] to access it.
    day = [d for d in sched_json["gameWeek"] if d["date"] == yesterday][0]

    #Since last four digits of game_id represent regular season order, so largest game_id is most recent game.
    #Find maximum game_id in yesterday's game data
    max_game_id = max([game["id"] for game in day["games"]])

    #Last four digits of maximum game_id yield number of games that have happened so far in the regular season.
    return max_game_id % 10000

#Lists of all required data for model
#Note: due to ciruclar import errors, this cannot go in constants.py
PBP_CODES = list(range(2024020001,2024021313)) + list(range(2025020001,2025020001+gtd()))

def write_play_by_play(game_id: int) -> None:
    """
    Pull play-by-play data from NHL API and write data to local system in JSON format.

    Args:
        game_id (int): id of game to pull play-by-play of
    """
    try:
        pbp = requests.get(f"https://api-web.nhle.com/v1/gamecenter/{game_id}/play-by-play", timeout=10)
        if pbp.status_code != 200:
            raise NetworkError(f"\033[91mCall to NHL API should yield status code 200, obtained status code {pbp.status_code} instead.\033[0m")
        pbp_json = pbp.json()

    except requests.exceptions.ConnectionError as exc:
        raise NetworkError(f"\033[91mResponse for game {game_id} unable to be received from API. Please check internet connection.\033[0m") from exc

    except requests.exceptions.Timeout as exc:
        raise ExcessDelayError("\033[91mResponse not received for API call within 10 seconds. Please check internet connection.\033[0m") from exc

    with open(constants.ROOT_DIRECTORY / "data" / "raw" /f"{game_id}.json", mode = "w", encoding="utf-8") as file:
        json.dump(pbp_json, file, indent=2)

def write_next_pbp() -> None:
    """
    Write oldest play-by-play data not yet in data/raw/ to JSON.
    """
    #Get list of all files in data/raw/
    current_files = os.listdir(constants.ROOT_DIRECTORY / "data" / "raw")
    #Cut off '.json' extension and cast to int to get game_id
    current_files = [int(file[:-5]) for file in current_files]
    #Find lowest game_id whose play-by-play we want for the model that isn't already in our raw dataset.
    try:
        next_file = [code for code in PBP_CODES if code not in current_files][0]

    except IndexError:
        print("\033[93mNo missing play-by-plays found to write. All required play-by-play data for model should be present.\033[0m")
        return None

    #Write this new play-by-play into our dataset
    write_play_by_play(next_file)

def clean_all_pbp() -> None:
    """
    Clean all raw data collected (including previously cleaned data).
    """
    #Get list of all files in data/raw/
    raw_files = os.listdir(constants.ROOT_DIRECTORY / "data" / "raw")

    for f in raw_files:
        #Get first file in raw/ but not in clean/; load respective JSON data to clean
        with open(constants.ROOT_DIRECTORY / "data" / "raw" / f"{f}", mode="r", encoding="utf-8") as file:
            pbp_json = json.load(file)
        #Clean data from this game
        pbp_json = clean_pbp(pbp_json)
        #Write cleaned data into clean/
        with open(constants.ROOT_DIRECTORY / "data" / "clean" /f"{f}", mode = "w", encoding="utf-8") as file:
            json.dump(pbp_json, file, indent=2)
