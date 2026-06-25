from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


def run_server(address: tuple[str, int], directory: str) -> None:
    
    class PyriteHandler(SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs) -> None:
            super().__init__(*args, directory=directory, **kwargs)

    with ThreadingHTTPServer(adderess, PyriteHandler) as httpd:
        print(f"Serving Pyrite at on {address[0]} on port {address[1]}")
        httpd.serve_forever()
