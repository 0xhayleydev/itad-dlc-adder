import random
import string
import requests
import json

from Exceptions import ResponseException
from IsThereAnyDeal.Config import Config
from IsThereAnyDeal.SteamGame import SteamGame
from Utils.Cache import Cache


class IsThereAnyDeal():
    @staticmethod
    def get_game(steam_app_id: str) -> SteamGame:
        url = f"https://api.isthereanydeal.com/games/lookup/v1?key={Config.API_KEY}&appid={steam_app_id}"

        steam_game = Cache.game_cache.get(url)

        if not steam_game:
            response = requests.get(url)

            if not response.status_code == 200:
                raise ResponseException(f"Could not find app with id: {steam_app_id}")
            
            steam_game = SteamGame.from_dict(json.loads(response.content))
            
            Cache.game_cache[url] = steam_game
        
        return steam_game