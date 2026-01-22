import json
from datetime import date

import pytest

from core import ingestion
from core import constants

params = [
    (2025020767, "raw"), #Sample game from 2025-2026 season (1/19/2026), should find in 'data/current'
    (2025020716, "raw"), #Sample game from 2025-2026 season (1/12/2026), should find in 'data/current'
    (2024020437,"raw"), #Sample game from 2024-2025 season (12/08/2024), should find in 'data/last'
    (2023030127,"raw"), #Sample playoff game from 2023-2024 playoffs (05/04/2024), should find in 'data/misc'
]

@pytest.mark.parametrize("game_id, folder", params)

def test_write_play_by_play(game_id: int, folder: str):
    ingestion.write_play_by_play(game_id, raw = True)

    #Open file previous call should have created.
    with open(constants.ROOT_DIRECTORY / "data" / folder / f"{game_id}.json", mode="r", encoding="utf-8") as file:
        data = json.load(file)

    assert data["id"] == game_id

@pytest.mark.parametrize("today, n_games", [
    (date(2026, 1, 19), 769),
    (date(2025, 10, 15), 56),
    (date(2025, 12, 31), 621),
])
def test_gtd(today: date, n_games: int):
    assert ingestion.gtd(today = today) == n_games
