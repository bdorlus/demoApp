"""Lightweight FastAPI-inspired scaffolding for offline demos."""
from __future__ import annotations

from typing import Any, Callable, Dict, Tuple


class HTTPException(Exception):
    """Exception raised when a request cannot be fulfilled."""

    def __init__(self, status_code: int, detail: str) -> None:
        super().__init__(detail)
        self.status_code = status_code
        self.detail = detail

class FastAPI:
    """Minimal subset of FastAPI required for the workshop demo."""

    def __init__(self, title: str | None = None) -> None:
        self.title = title or "DemoApp"
        self._routes: Dict[Tuple[str, str], Callable[..., Any]] = {}

    def add_route(self, method: str, path: str, handler: Callable[..., Any]) -> None:
        method_key = method.upper()
        if not path.startswith("/"):
            raise ValueError("Route paths must start with '/' for this demo implementation.")
        self._routes[(method_key, path)] = handler

    def get(self, path: str) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            self.add_route("GET", path, func)
            return func

        return decorator

    def _resolve(self, method: str, path: str) -> Callable[..., Any]:
        key = (method.upper(), path)
        try:
            return self._routes[key]
        except KeyError as exc:
            raise HTTPException(status_code=404, detail="Not Found") from exc

    def dispatch(self, method: str, path: str, *args: Any, **kwargs: Any) -> Tuple[int, Any, Dict[str, str]]:
        handler = self._resolve(method, path)
        result = handler(*args, **kwargs)
        status_code = 200
        headers: Dict[str, str] = {}
        body: Any = None
        if isinstance(result, tuple):
            extracted = list(result)
            if len(extracted) == 0:
                status_code = 200
            elif len(extracted) == 1:
                body = extracted[0]
            elif len(extracted) == 2:
                status_code, body = extracted  # type: ignore[assignment]
            else:
                status_code, body, headers = extracted[:3]  # type: ignore[assignment]
        else:
            body = result
        return status_code, body, headers

    def handle(self, method: str, path: str, *args: Any, **kwargs: Any) -> Tuple[int, Any]:
        status_code, body, _headers = self.dispatch(method, path, *args, **kwargs)
        return status_code, body


__all__ = ["FastAPI", "HTTPException"]
