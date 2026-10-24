import copy
import re
from typing import Generator, List, Dict, Tuple
from src.config.settings import settings
from src.domain.enums import AgentRole
from src.domain.schemas import CaseFile, CourtTurn
from src.prompts.templates import PromptFactory
from src.services.llm_provider import GroqCourtroomProvider

class CourtroomOrchestrator:
    def __init__(self, llm_provider: GroqCourtroomProvider):
        self.llm = llm_provider

    def _build_perspective_history(
        self, transcript: List[CourtTurn], active_role: AgentRole
    ) -> List[Dict[str, str]]:
        history = []
        remaining_chars = getattr(settings, "MAX_CONTEXT_CHARS", 12000)

        # Exclude the currently streaming turn (the last element)
        for turn in transcript[:-1]:
            if not turn.statement or not turn.statement.strip():
                continue

            statement = turn.statement[-2600:]
            # If the turn belongs to the active role, treat as assistant (their past statements),
            # otherwise treat as user (opponent/court statements).
            role_tag = "assistant" if turn.role == active_role else "user"
            prefix = f"[Round {turn.round_number} - {turn.role.value}]: "
            content = prefix + statement

            if len(content) > remaining_chars:
                break

            history.append({"role": role_tag, "content": content})
            remaining_chars -= len(content)

        return history

    def _snapshot(self, case: CaseFile) -> CaseFile:
        return copy.deepcopy(case)

    @staticmethod
    def extract_evidence_locker(transcript: List[CourtTurn]) -> str:
        """Extracts bracketed Exhibits from the transcript for the Evidence Locker sidebar."""
        exhibits = []
        pattern = re.compile(r"\[([^\]]*Exhibit[^\]]*)\]", re.IGNORECASE)
        for turn in transcript:
            if not turn.statement:
                continue
            matches = pattern.findall(turn.statement)
            for match in matches:
                icon = "🔴" if turn.role == AgentRole.PROSECUTION else "🔵"
                exhibits.append(f"- {icon} **Round {turn.round_number}**: `[{match}]`")
        return "\n".join(exhibits) if exhibits else "*No exhibits logged yet...*"

    def run_trial(
        self,
        country: str,
        crime: str,
        num_rounds: int,
        prosecutor_model: str,
        defense_model: str,
        jury_model: str,
    ) -> Generator[Tuple[CaseFile, str], None, None]:
        safe_rounds = min(max(1, num_rounds), settings.MAX_ROUNDS)
        case = CaseFile(country=country, crime=crime, max_rounds=safe_rounds)

        prosecutor_sys = PromptFactory.build_prosecutor_system_prompt(country, crime)
        defense_sys = PromptFactory.build_defense_system_prompt(country, crime)
        jury_sys = PromptFactory.build_jury_system_prompt(country, crime)

        for current_round in range(1, safe_rounds + 1):
            # --- 1. Opposition Prosecutor Turn ---
            pros_turn = CourtTurn(current_round, AgentRole.PROSECUTION, prosecutor_model, "")
            case.transcript.append(pros_turn)

            pros_history = self._build_perspective_history(case.transcript, AgentRole.PROSECUTION)
            prompt_msg = (
                f"The court is in session for {country}. Present your opening indictment and statistical evidence for: '{crime}'."
                if current_round == 1
                else f"Round {current_round}/{safe_rounds}: Rebut the Defense's statistics and introduce a new numbered [Exhibit]."
            )
            pros_history.append({"role": "user", "content": prompt_msg})

            for partial_text in self.llm.stream_turn(prosecutor_model, prosecutor_sys, pros_history):
                pros_turn.statement = partial_text
                yield self._snapshot(case), self.extract_evidence_locker(case.transcript)

            # --- 2. Government Defense Turn ---
            def_turn = CourtTurn(current_round, AgentRole.DEFENSE, defense_model, "")
            case.transcript.append(def_turn)

            def_history = self._build_perspective_history(case.transcript, AgentRole.DEFENSE)
            def_history.append({
                "role": "user",
                "content": f"Round {current_round}/{safe_rounds}: Counter the Prosecution's exhibit using official state data from {country} and log a [Defense Exhibit]."
            })

            for partial_text in self.llm.stream_turn(defense_model, defense_sys, def_history):
                def_turn.statement = partial_text
                yield self._snapshot(case), self.extract_evidence_locker(case.transcript)

        # --- 3. Structured Jury Verdict ---
        full_transcript_text = "\n\n".join(
            [f"Round {t.round_number} ({t.role.value}):\n{t.statement[-2200:]}" for t in case.transcript if t.statement]
        )[-getattr(settings, "MAX_VERDICT_CONTEXT_CHARS", 12000):]

        case.verdict_report = self.llm.generate_structured_verdict(
            model=jury_model,
            system_prompt=jury_sys,
            transcript_prompt=f"Country: {country}\nIndictment: {crime}\n\nTranscript:\n{full_transcript_text}",
        )
        yield self._snapshot(case), self.extract_evidence_locker(case.transcript)