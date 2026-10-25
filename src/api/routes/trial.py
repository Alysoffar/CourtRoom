import asyncio
import time
from typing import Any, Iterator

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from src.config.settings import settings
from src.config.trial_options import PRESET_CRIMES
from src.domain.enums import AgentRole
from src.domain.schemas import CaseFile
from src.services.llm_provider import GroqCourtroomProvider
from src.services.orchestrator import CourtroomOrchestrator

router = APIRouter()


def _next_update(trial: Iterator[tuple[CaseFile, str]]) -> tuple[CaseFile, str] | None:
    try:
        return next(trial)
    except StopIteration:
        return None


def _trial_options(params: dict[str, Any]) -> dict[str, Any]:
    return {
        "country": (params.get("country") or "Egypt").strip(),
        "crime": (params.get("crime") or PRESET_CRIMES[0]).strip(),
        "num_rounds": int(params.get("rounds") or 3),
        "prosecutor_model": params.get("pros_model")
        or settings.DEFAULT_PROSECUTOR_MODEL,
        "defense_model": params.get("def_model") or settings.DEFAULT_DEFENSE_MODEL,
        "jury_model": params.get("jury_model") or settings.DEFAULT_JURY_MODEL,
    }


def _create_orchestrator() -> CourtroomOrchestrator:
    api_key = settings.GROQ_API_KEY.strip()
    if not api_key:
        raise ValueError("Set GROQ_API_KEY in your .env file first.")
    return CourtroomOrchestrator(GroqCourtroomProvider(api_key=api_key))


def _transcript(case: CaseFile) -> list[dict[str, Any]]:
    return [
        {
            "round_number": turn.round_number,
            "role_key": "PROSECUTION"
            if turn.role == AgentRole.PROSECUTION
            else "DEFENSE",
            "role_label": turn.role.value,
            "statement": turn.statement,
        }
        for turn in case.transcript
        if turn.statement and turn.statement.strip()
    ]


def _payload(case: CaseFile, evidence: str) -> dict[str, Any]:
    turn = case.transcript[-1]
    complete = bool(case.verdict_report)
    if complete:
        role, title, label = "JURY", "SUPREME JURY · FINAL VERDICT", "VERDICT DELIVERED"
        dialogue = latest = case.verdict_report
    else:
        prosecution = turn.role == AgentRole.PROSECUTION
        role = "PROSECUTION" if prosecution else "DEFENSE"
        title = (
            f"OPPOSITION PROSECUTOR · ROUND {turn.round_number}"
            if prosecution
            else f"GOVERNMENT DEFENSE · ROUND {turn.round_number}"
        )
        label = f"ROUND {turn.round_number} OF {case.max_rounds}"
        dialogue = turn.statement or "*Taking the podium...*"
        latest = turn.statement

    return {
        "active_role": role,
        "speaker_title": title,
        "round_label": label,
        "dialogue_text": dialogue,
        "latest_statement": latest,
        "transcript": _transcript(case),
        "evidence_md": evidence,
        "verdict_md": case.verdict_report or "*Deliberation in progress...*",
        "is_complete": complete,
    }


@router.websocket("/ws/trial")
async def trial_websocket(websocket: WebSocket) -> None:
    await websocket.accept()
    try:
        options = _trial_options(await websocket.receive_json())
        trial = _create_orchestrator().run_trial(**options)
        last_count = 0
        last_sent = 0.0

        while update := await asyncio.to_thread(_next_update, trial):
            case, evidence = update
            now = time.monotonic()
            complete = bool(case.verdict_report)
            changed = len(case.transcript) != last_count
            if not complete and not changed and now - last_sent < 0.035:
                continue
            await websocket.send_json(_payload(case, evidence))
            last_count, last_sent = len(case.transcript), now
            await asyncio.sleep(0)
    except WebSocketDisconnect:
        pass
    except Exception as exc:
        await websocket.send_json({"error": str(exc)})
