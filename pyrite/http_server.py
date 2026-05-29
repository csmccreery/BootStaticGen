from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


class PyriteHandler(SimpleHTTPRequestHandler):
    def __init__(self,  directory: str, *args, **kwargs)-> None:
        super().__init__(*args, directory=directory, **kwargs)


def run_server(address: tuple[str, int], directory: str) -> None:
    pass
