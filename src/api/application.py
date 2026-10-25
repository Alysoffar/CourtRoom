from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.api.routes.static import router as static_router
from src.api.routes.tts import router as tts_router
from src.api.routes.trial import router as trial_router
from src.services.tts_provider import LocalSpeechProvider


def create_app() -> FastAPI:
    """Build the application and wire its transport-level dependencies."""
    app = FastAPI(title="The Sovereign Tribunal 3D")
    ui_path = Path(__file__).parents[2] / "src" / "ui"
    app.state.html_path = ui_path / "courtroom.html"
    app.state.speech_provider = LocalSpeechProvider()
    app.mount("/static", StaticFiles(directory=ui_path / "static"), name="static")

    app.include_router(static_router)
    app.include_router(tts_router)
    app.include_router(trial_router)
    return app
