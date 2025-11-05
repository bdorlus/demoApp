"""Tiny HTTP runner compatible with the DemoApp FastAPI shim."""
from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any
from urllib.parse import urlparse

from fastapi import FastAPI, HTTPException


class _Handler(BaseHTTPRequestHandler):
    app: FastAPI | None = None

    def do_GET(self) -> None:  # noqa: N802 (method name per BaseHTTPRequestHandler API)
        self._handle("GET")

    def _handle(self, method: str) -> None:
        assert self.app is not None, "Application not attached to handler"
        parsed = urlparse(self.path)
        try:
            status_code, body, headers = self.app.dispatch(method, parsed.path)
        except HTTPException as exc:
            status_code, body, headers = exc.status_code, {"detail": exc.detail}, {}

        payload: bytes
        content_type = "text/plain; charset=utf-8"
        if body is None:
            payload = b""
        elif isinstance(body, (bytes, bytearray)):
            payload = bytes(body)
            content_type = "application/octet-stream"
        elif isinstance(body, (dict, list)):
            payload = json.dumps(body).encode("utf-8")
            content_type = "application/json"
        else:
            payload = str(body).encode("utf-8")

        self.send_response(status_code)
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("Content-Type", content_type)
        for key, value in headers.items():
            self.send_header(key, value)
        self.end_headers()
        if payload:
            self.wfile.write(payload)

    def log_message(self, format: str, *args: Any) -> None:
        # Keep CLI output quiet to mirror uvicorn's default concise logging.
        return


def run(app: FastAPI, *, host: str = "127.0.0.1", port: int = 8000, reload: bool | None = None) -> None:
    """Start a simple HTTP server bound to the provided application."""

    _Handler.app = app
    server = ThreadingHTTPServer((host, port), _Handler)
    print(f"Demo server running on http://{host}:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("Shutting down...")
    finally:
        server.server_close()
