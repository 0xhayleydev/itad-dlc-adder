from typing import Any

class ResponseException(Exception):
    def __init__(self, t: Any, obj: Any):
        super.__init__(self, t, obj)