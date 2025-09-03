from IsThereAnyDeal.SteamGame import SteamGame


class Cache():
    _games: dict[str, SteamGame] = {}

    @classmethod
    def get_game(cls, url: str) -> SteamGame | None:
        return cls._games.get(url)

    @classmethod
    def add_game(cls, url: str, game: SteamGame) -> None:
        cls._games[url] = game
