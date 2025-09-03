import json

import requests

from Exceptions.ResponseError import ResponseError
from IsThereAnyDeal.Config import Config
from IsThereAnyDeal.SteamGame import SteamGame
from Utils.Cache import Cache


class IsThereAnyDeal():
    @staticmethod
    def get_game(steam_app_id: str) -> SteamGame:
        url = f"{Config.ITAD_API_URI}/games/lookup/v1?key={Config.API_KEY}&appid={steam_app_id}"

        steam_game = Cache.get_game(url)

        if not steam_game:
            response = requests.get(url, timeout=60)

            if not response.status_code == 200:
                raise ResponseError(f"Could not find app with id: {steam_app_id}")

            steam_game = SteamGame.from_dict(json.loads(response.content))

            Cache.add_game(url, steam_game)

        return steam_game

    @staticmethod
    def get_dlc(steam_app_id: str) -> SteamGame | None:
        pass
