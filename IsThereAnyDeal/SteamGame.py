from __future__ import annotations

from enum import Enum
from typing import TypeAlias
import requests

from Exceptions import ResponseException
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
    
    def __init__(self, found: bool = False, id: NullableStr = None, slug: NullableStr = None, title: NullableStr = None, game_type: GameType | None = None) -> None:
        self.found = found
        self.id = id
        self.slug = slug
        self.title = title
        self.game_type = game_type

    def from_dict(data: dict) -> SteamGame:
        found = data.get("found")

        if not found:
            return SteamGame(False)
        
        game_data: dict = data.get("game")
        id = game_data.get("id")
        slug = game_data.get("slug")
        title = game_data.get("title")
        type = GameType(game_data.get("type"))

        return SteamGame(True, id, slug, title, type)
    
    def get_dlc_list(self):
        url = f"https://isthereanydeal.com/api/game/info/?key={Config.API_KEY}"

        data = {"gid": self.id}

        response = requests.post(url, json=data)

        if not response.status_code == 200:
            raise ResponseException(f"Could not dlc for: '{self.title}'")
        
        data = response.json()

        print(data)