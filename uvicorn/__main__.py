"""Command line interface for the demo uvicorn shim."""
from __future__ import annotations

import argparse
import importlib

from . import run


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="uvicorn")
    parser.add_argument("app", help="Target application in module:object notation")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--reload", action="store_true", help="Ignored; maintained for compatibility")
    args = parser.parse_args(argv)

    module_name, _, attr = args.app.partition(":")
    if not module_name or not attr:
        raise SystemExit("app must be specified as module:object")

    module = importlib.import_module(module_name)
    try:
        app = getattr(module, attr)
    except AttributeError as exc:
        raise SystemExit(f"Could not find '{attr}' on module '{module_name}'") from exc

    run(app, host=args.host, port=args.port, reload=args.reload)


if __name__ == "__main__":
    main()
