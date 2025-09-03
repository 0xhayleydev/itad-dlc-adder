from __future__ import annotations


from http.server import BaseHTTPRequestHandler, HTTPServer

from threading import Thread
from typing import Tuple
from urllib import parse as urlparse

from IsThereAnyDeal.Config import Config

class OAuthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse.urlparse(self.path)
        params = urlparse.parse_qs(parsed.query)

        code = params.get("code")
        
        if parsed.path == f"/{Config.REDIRECT_CALLBACK}" and code:
            self.server.auth_code = code[0]
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers
            self.wfile.write(b"Authorization complete! You can close this window.")
        else:
            self.send_response(400)
            self.end_headers()

    @staticmethod
    def start_listening() -> Tuple[HTTPServer, Thread]:
        server = HTTPServer((Config.REDIRECT_HOSTNAME, Config.REDIRECT_PORT), OAuthHandler)
        thread = Thread(target=server.handle_request)
        thread.start()

        return server, thread

