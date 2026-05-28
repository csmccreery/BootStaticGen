import http.server as srv
from pathlib import Path

class PyriteServer(srv.ThreadingHTTPServer):
    def __init__(self, address: tuple[str, str], path: str) -> None:
        super().__init__(address, None)
