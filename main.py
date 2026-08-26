import os
import socket
from healthtech import app


def find_free_port(start: int = 5008, end: int = 5018) -> int:
    for port in range(start, end + 1):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                sock.bind(("127.0.0.1", port))
                return port
            except OSError:
                continue
    raise RuntimeError("No free ports available between 5008 and 5018")


if __name__ == "__main__":
    requested_port = int(os.environ.get("PORT", 5008))
    try:
        port = find_free_port(requested_port, requested_port + 10)
    except RuntimeError:
        port = find_free_port(5008, 5018)
    if port != requested_port:
        print(f"Port {requested_port} is busy. Starting on port {port} instead.")
    app.run(port=port)
