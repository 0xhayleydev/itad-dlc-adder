

from base64 import urlsafe_b64encode
from hashlib import sha256
import re
import webbrowser

import requests
import urllib

from IsThereAnyDeal.Config import Config
from Utils.OAuthUtils.OAuthHandler import OAuthHandler
from Utils.StringUtils import StringUtils


class OAuth():
    class OAuthToken():
        key: str
    
    @staticmethod
    def base64_url(input: str) -> str:
        digest = sha256(input.encode()).digest()
        value = urlsafe_b64encode(digest).decode('utf-8')
        return value.rstrip('=')
    
    @staticmethod
    def authenticate_user() -> OAuthToken | None:
        server, thread = OAuthHandler.start_listening()

        verifier = StringUtils.generate_string(64)

        OAuth.generate_code(verifier)

        thread.join()

        code = getattr(server, "auth_code", None)
        if not code:
            return None

        return OAuth.get_token(verifier, code)

    @staticmethod
    def generate_code(verifier: str) -> None:
        state = StringUtils.generate_string(30)

        params = {
            "response_type": "code",
            "client_id": Config.CLIENT_ID,
            "redirect_uri": Config.REDIRECT_URI,
            "scope": ' '.join(Config.REQUIRED_SCOPES),
            "state": state,
            "code_challenge": OAuth.base64_url(verifier),
            "code_challenge_method": "S256"
        }

        webbrowser.open(f"{Config.ITAD_URI}/oauth/authorize/?{urllib.parse.urlencode(params)}")


    @staticmethod
    def get_token(verifier: str, code: str):
        data = {
            "grant_type": "authorization_code",
            "client_id": Config.CLIENT_ID,
            "redirect_uri": Config.REDIRECT_URI,
            "code": code,
            "code_verifier": verifier
        }

        response = requests.post(f"{Config.ITAD_URI}/oauth/token/", json=data)

        print(response)