from __future__ import annotations

from enum import Enum
from typing import Any, TypeAlias

import requests

from Exceptions.ResponseError import ResponseError
from IsThereAnyDeal.Config import Config

NullableStr: TypeAlias = str | None

class GameType(Enum):
    GAME = "game"
    DLC = "dlc"
    PACKAGE = "package"

class SteamGame():
    found: bool = False
    id: NullableStr = None
    slug: NullableStr = None
    title: NullableStr = None
    game_type: GameType | None = None

    def __init__(self) -> None:
        self.found = False
        self.id = None
        self.slug = None
        self.title = None
        self.game_type = None

    @staticmethod
    def from_dict(data: dict[str, Any]) -> SteamGame:
        game = SteamGame()

        game.found = bool(data.get("found"))

        if game.found:
            game_data: dict = dict(data.get("game", {}))
            game.id = str(game_data.get("id", "Invalid ID"))
            game.slug = str(game_data.get("slug", "invalid-slug"))
            game.title = str(game_data.get("title", "Invalid Title"))
            game.game_type = GameType(game_data.get("type"))

        return game

    def get_dlc_list(self):
        url = f"https://isthereanydeal.com/api/game/info/?key={Config.API_KEY}"

        data = {"gid": self.id}

        response = requests.post(url, json=data, timeout=60)

        if not response.status_code == 200:
            raise ResponseError(f"Could not dlc for: '{self.title}'")

        data = response.json()

        print(data)
