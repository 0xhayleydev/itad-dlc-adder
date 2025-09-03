from __future__ import annotations

import json
from pathlib import Path


class Config():
    _config: Config | None = None

    CLIENT_ID = ""
    CLIENT_SECRET = ""
    API_KEY = ""

    REDIRECT_HOSTNAME = "localhost"
    REDIRECT_PORT = 8080
    REDIRECT_CALLBACK = "callback"

    REDIRECT_URI = f"http://{REDIRECT_HOSTNAME}:{REDIRECT_PORT}/{REDIRECT_CALLBACK}"

    REQUIRED_SCOPES = [
        "wait_read",
        "wait_write",
        "coll_read",
        "coll_write",
        "notes_read",
        "notes_write"
    ]

    ITAD_URI = "https://isthereanydeal.com"
    ITAD_API_URI = "https://api.isthereanydeal.com"

    @classmethod
    def load(cls, config_file: Path) -> Config | None:
        if not cls._config:
            cls.reload(config_file)

        return cls._config

    @classmethod
    def reload(cls, config_file: Path) -> Config:
        with open(config_file, encoding="utf-8") as file:
            data = dict(json.loads(file.read()))
            cls.CLIENT_ID = str(data.get("client_id"))
            cls.CLIENT_SECRET = str(data.get("client_secret"))
            cls.API_KEY = str(data.get("api_key"))
            cls._config = cls()

        return cls._config
