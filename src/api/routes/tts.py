import asyncio

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import FileResponse
from pydantic import BaseModel

router = APIRouter()


class TTSRequest(BaseModel):
    text: str


@router.post("/api/tts")
async def synthesize_speech(request: Request, payload: TTSRequest) -> FileResponse:
    if not payload.text.strip():
        raise HTTPException(status_code=400, detail="Empty text")

    audio_path = await asyncio.to_thread(
        request.app.state.speech_provider.synthesize,
        payload.text,
    )
    if not audio_path:
        raise HTTPException(status_code=500, detail="TTS synthesis failed")
    return FileResponse(audio_path, media_type="audio/wav")
