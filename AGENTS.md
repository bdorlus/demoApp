# Repository Guidelines

## Project Structure & Module Organization
- Place all FastAPI code under `app/`; `app/main.py` should expose the `FastAPI` instance and register routers.
- Add new feature modules inside `app/` (e.g., `app/routes/status.py`) and import them from `main.py`.
- Keep shared utilities in `app/services/` or `app/dependencies.py` to avoid circular imports.
- Mirror application layout in `tests/`; name modules like `tests/test_status.py` and share fixtures in `tests/conftest.py`.
- Track config and dependency pins in `requirements.txt`; update it with any new package and regenerate the lock step if you add one.

## Build, Test, and Development Commands
- `python -m venv .venv && source .venv/bin/activate` prepares an isolated environment before installing dependencies.
- `make install` (defined in the workshop Makefile) should install `requirements.txt` and freeze the environment; keep this target current when dependencies change.
- `make build` is reserved for packaging or lint steps—extend it rather than creating ad-hoc scripts.
- `make run` should keep launching `uvicorn app.main:app --reload` for local development; verify log output after changes.
- `python -m pytest` runs the unit suite; if you add a dedicated `make test` alias, wire it to this command.

## Coding Style & Naming Conventions
- Target Python 3.11+, follow PEP 8 with 4-space indentation, and prefer explicit type hints on public functions.
- Use snake_case for variables and functions, PascalCase for Pydantic models and classes, and kebab-case for filenames exposed via scripts.
- Organize settings with `pydantic.BaseSettings` (e.g., `app/config.py`) and keep FastAPI routers in `app/routes/` when growth warrants.
- Run formatters before committing; if you adopt `black` or `ruff`, add the invocation to `make build` and document it here.

## Testing Guidelines
- Write tests with `pytest` and FastAPI's `TestClient`; each new endpoint should ship with at least happy-path and failure tests.
- Name tests using `test_<unit_under_test>_<expected_behavior>` and isolate networking via dependency overrides or fixtures.
- Run `pytest --maxfail=1 --disable-warnings` locally; capture coverage using `pytest --cov=app` when enforcing thresholds.

## Commit & Pull Request Guidelines
- Use concise, imperative commit subjects (~50 chars) similar to existing history (`Add status endpoint`, `Create install target`).
- Group refactors, features, and formatting changes into separate commits to simplify review.
- Pull requests must describe the change, link relevant issues or tickets, and include evidence (e.g., `pytest` output or `curl http://localhost:8000/status`).
- Request at least one peer review before merging; ensure CI (or local equivalents) is green and reference any follow-up work clearly.
