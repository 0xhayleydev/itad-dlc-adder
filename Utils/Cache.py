from IsThereAnyDeal.SteamGame import SteamGame


class Cache():
    game_cache: dict[str, SteamGame] = {}