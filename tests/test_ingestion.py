import json
from datetime import date

import pytest

from core import ingestion
from core import constants

game_ids = [
    2025020767, #Sample game from 2025-2026 season (1/19/2026)
    2025020716, #Sample game from 2025-2026 season (1/12/2026)
    2024020437, #Sample game from 2024-2025 season (12/08/2024)
    2023030127, #Sample playoff game (05/04/2024)
]

@pytest.mark.parametrize("game_id", game_ids)

def test_write_play_by_play(game_id: int):
    ingestion.write_play_by_play(game_id)
    #Open file previous call should have created.
    with open(constants.ROOT_DIRECTORY / "data" / "play-by-play" / f"{game_id}.json", mode="r", encoding="utf-8") as file:
        data = json.load(file)

    assert data["id"] == game_id

@pytest.mark.parametrize("today, n_games", [
    (date(2026, 1, 19), 769),
    (date(2025, 10, 15), 56),
    (date(2025, 12, 31), 621),
])
def test_gtd(today: date, n_games: int):
    assert ingestion.gtd(today = today) == n_games
