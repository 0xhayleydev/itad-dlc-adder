from __future__ import annotations

import base64
import hashlib
import urllib
import webbrowser
from dataclasses import dataclass
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread
from typing import Tuple
from urllib import parse as urlparse

import requests

from IsThereAnyDeal.Config import Config
from Utils.StringUtils import StringUtils


class OAuth():
    @dataclass
    class Token():
        token_type: str
        expires_in: int
        access_token: str
        refresh_token: str

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            parsed = urlparse.urlparse(self.path)
            params = urlparse.parse_qs(parsed.query)

            code = params.get("code")

            if parsed.path == f"/{Config.REDIRECT_CALLBACK}" and code:
                self.server.auth_code = code[0]
                self.send_response(200)
                self.send_header("Content-Type", "text/html")
                self.end_headers()
                self.wfile.write(b"Authorization complete! You can close this window.")
            else:
                self.send_response(400)
                self.end_headers()

        @staticmethod
        def start_listening() -> Tuple[HTTPServer, Thread]:
            server = HTTPServer((Config.REDIRECT_HOSTNAME, Config.REDIRECT_PORT), OAuth.Handler)
            thread = Thread(target=server.handle_request)
            thread.start()

            return server, thread

    @staticmethod
    def base64_urlsafe(input_string: str) -> str:
        digest = hashlib.sha256(input_string.encode()).digest()
        value = base64.urlsafe_b64encode(digest).decode('utf-8')
        return value.rstrip('=')

    @classmethod
    def authenticate_user(cls) -> Token | None:
        server, thread = OAuth.Handler.start_listening()

        verifier = StringUtils.generate_string(64)

        cls.generate_code(verifier)

        thread.join()

        code = getattr(server, "auth_code", None)
        if not code:
            return None

        return cls.get_token(verifier, code)

    @classmethod
    def generate_code(cls, verifier: str) -> None:
        state = StringUtils.generate_string(30)

        params = {
            "response_type": "code",
            "client_id": Config.CLIENT_ID,
            "redirect_uri": Config.REDIRECT_URI,
            "scope": ' '.join(Config.REQUIRED_SCOPES),
            "state": state,
            "code_challenge": cls.base64_urlsafe(verifier),
            "code_challenge_method": "S256"
        }

        webbrowser.open(f"{Config.ITAD_URI}/oauth/authorize/?{urllib.parse.urlencode(params)}")


    @staticmethod
    def get_token(verifier: str, code: str) -> OAuth.Token | None:
        data = {
            "grant_type": "authorization_code",
            "client_id": Config.CLIENT_ID,
            "redirect_uri": Config.REDIRECT_URI,
            "code": code,
            "code_verifier": verifier
        }

        response = requests.post(f"{Config.ITAD_URI}/oauth/token/", data=data, timeout=30)

        try:
            return OAuth.Token(**response.json())
        except TypeError as e:
            print(f"Failed to create Token due to '{e}'")

        return None
