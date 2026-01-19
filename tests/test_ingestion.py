import json

import pytest

from core.ingestion import write_play_by_play
from core import constants

@pytest.mark.parametrize("game_id", [
    2025020767, #Sample game from 2025-2026 season (1/19/2026)
    2025020716, #Sample game from 2025-2026 season (1/12/2026)
    2024020437, #Sample game from 2024-2025 season (12/08/2024)
    2023030127, #Sample playoff game (05/02/2024)
])

def test_write_play_by_play(game_id: int):
    write_play_by_play(game_id)
    #Open file previous call should have created.
    with open(constants.ROOT_DIRECTORY / "data" / "play-by-play" / f"{game_id}.json", mode="r", encoding="utf-8") as file:
        data = json.load(file)

    assert data["id"] == game_id
