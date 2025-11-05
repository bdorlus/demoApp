"""Simplified TestClient compatible with the demo FastAPI shim."""
from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

from . import FastAPI, HTTPException


@dataclass
class Response:
    status_code: int
    body: Any

    def json(self) -> Any:
        return self.body

    @property
    def text(self) -> str:
        if isinstance(self.body, (dict, list)):
            return json.dumps(self.body)
        return str(self.body)


class TestClient:
    """Minimal test client that executes handlers directly."""

    def __init__(self, app: FastAPI) -> None:
        self.app = app

    def get(self, path: str) -> Response:
        return self._request("GET", path)

    def _request(self, method: str, path: str) -> Response:
        try:
            status_code, body = self.app.handle(method, path)
        except HTTPException as exc:
            status_code, body = exc.status_code, {"detail": exc.detail}
        return Response(status_code=status_code, body=body)
