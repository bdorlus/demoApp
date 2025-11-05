"""DemoApp FastAPI application entry point."""
from fastapi import FastAPI

app = FastAPI(title="DemoApp")


@app.get("/status")
def read_status() -> dict[str, str]:
    """Return service health metadata."""
    return {"status": "ok", "app": "DemoApp"}
