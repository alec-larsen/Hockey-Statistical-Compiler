import json
from datetime import date

import pytest

from core import ingestion
from core import constants

params = [
    2025020767, #Sample game from 2025-2026 season (1/19/2026), should find in 'data/current'
    2025020716, #Sample game from 2025-2026 season (1/12/2026), should find in 'data/current'
    2024020437, #Sample game from 2024-2025 season (12/08/2024), should find in 'data/last'
    2023030127, #Sample playoff game from 2023-2024 playoffs (05/04/2024), should find in 'data/misc'
    2025020796, #Sample regular season game from 2025-2026; went to shootout.
]

#Test writing play-by-plays
@pytest.mark.parametrize("game_id", params)
def test_write_play_by_play(game_id: int):
    ingestion.write_play_by_play(game_id)

    #Open file previous call should have created.
    with open(constants.ROOT_DIRECTORY / "data" / "raw" / f"{game_id}.json", mode="r", encoding="utf-8") as file:
        data = json.load(file)

    assert data["id"] == game_id

#Test game counting
@pytest.mark.parametrize("today, n_games", [
    (date(2026, 1, 19), 769),
    (date(2025, 10, 15), 56),
    (date(2025, 12, 31), 621),
])
def test_gtd(today: date, n_games: int):
    assert ingestion.gtd(today = today) == n_games

@pytest.mark.parametrize("game_id", params)

def test_clean_pbp_keys(game_id: int):
    with open(constants.ROOT_DIRECTORY / "data" / "raw" / f"{game_id}.json", mode="r", encoding="utf-8") as file:
        data = json.load(file)

    data = ingestion.clean_pbp(data)

    #Get all keys for cleaned data dict as strings for easy comparison
    data_keys = [str(k) for k in data.keys()]

    assert data_keys == constants.CLEAN_MAIN_KEYS
