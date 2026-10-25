from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from src.config.settings import settings
from src.config.trial_options import PRESET_CRIMES

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def serve_courtroom(request: Request) -> str:
    return request.app.state.html_path.read_text(encoding="utf-8")


@router.get("/api/config")
async def get_config() -> dict[str, object]:
    return {
        "preset_crimes": PRESET_CRIMES,
        "models": settings.AVAILABLE_MODELS,
        "default_pros": settings.DEFAULT_PROSECUTOR_MODEL,
        "default_def": settings.DEFAULT_DEFENSE_MODEL,
        "default_jury": settings.DEFAULT_JURY_MODEL,
        "max_rounds": settings.MAX_ROUNDS,
    }
