import json
import re
from typing import List, Dict, Generator
from groq import Groq, RateLimitError, APIError
from src.config.settings import settings
from src.domain.schemas import JuryVerdictSchema


class GroqCourtroomProvider:
    def __init__(self, api_key: str):
        self.client = Groq(
            api_key=api_key,
            max_retries=getattr(settings, "MAX_RETRIES", 3),
        )

    @staticmethod
    def _clean_thinking(text: str) -> str:
        """Strips inline <think>...</think> blocks if present."""
        if "<think>" not in text:
            return text
        if "</think>" not in text:
            return ""
        return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()

    @staticmethod
    def _resolve_verdict(parsed: JuryVerdictSchema) -> str:
        """Apply the courtroom scoring rule instead of trusting inconsistent model output."""
        prosecution_score = parsed.prosecution_score
        defense_score = parsed.defense_score

        if prosecution_score >= 7 and prosecution_score - defense_score >= 2:
            return "GUILTY"
        if defense_score >= 7 and defense_score - prosecution_score >= 2:
            return "NOT GUILTY"

        verdict = parsed.verdict.strip().upper()
        return "NOT GUILTY" if verdict == "NOT GUILTY" else "GUILTY"

    def stream_turn(
        self, model: str, system_prompt: str, messages: List[Dict[str, str]]
    ) -> Generator[str, None, None]:
        """Streams tokens in real-time from Groq's LPU with low reasoning effort for instant output."""
        payload = [{"role": "system", "content": system_prompt}] + messages

        req_kwargs = {
            "model": model,
            "messages": payload,
            "temperature": settings.TEMPERATURE,
            "max_completion_tokens": settings.MAX_COMPLETION_TOKENS,
            "reasoning_effort": "low",
            "stream": True,
        }

        try:
            try:
                stream = self.client.chat.completions.create(**req_kwargs)
            except (TypeError, APIError):
                # Fallback if a specific model doesn't support the reasoning_effort param
                req_kwargs.pop("reasoning_effort", None)
                stream = self.client.chat.completions.create(**req_kwargs)

            partial_text = ""
            reasoning_fallback = ""

            for chunk in stream:
                if not chunk.choices:
                    continue
                delta_obj = chunk.choices[0].delta
                if not delta_obj:
                    continue

                content_piece = getattr(delta_obj, "content", None)
                if content_piece:
                    partial_text += content_piece
                    cleaned = self._clean_thinking(partial_text)
                    if cleaned:
                        yield cleaned
                else:
                    r_piece = getattr(delta_obj, "reasoning", None)
                    if r_piece:
                        reasoning_fallback += r_piece

            final_cleaned = self._clean_thinking(partial_text).strip()
            if not final_cleaned and reasoning_fallback.strip():
                yield reasoning_fallback.strip()

        except RateLimitError as e:
            raise RuntimeError(f"Groq Free Tier Rate Limit reached. Please wait a few seconds: {e}")
        except APIError as e:
            if getattr(e, "status_code", None) == 413:
                raise RuntimeError(
                    "This courtroom request exceeded Groq's free-tier token limit. "
                    "Use fewer trial rounds or openai/gpt-oss-20b."
                ) from e
            raise RuntimeError(f"Groq API Error: {e}")

    def generate_structured_verdict(
        self, model: str, system_prompt: str, transcript_prompt: str
    ) -> str:
        """Uses Groq's JSON mode + Pydantic validation to generate an air-tight Jury Verdict."""
        schema_json = json.dumps(
            JuryVerdictSchema.model_json_schema(), separators=(",", ":")
        )
        strict_system = (
            f"{system_prompt}\n"
            "Return one complete JSON object. Do not use Markdown, code fences, or "
            "additional text. Keep every analysis and the sentence under 35 words.\n"
            f"Required JSON schema:\n{schema_json}"
        )
        req_kwargs = {
            "model": model,
            "messages": [
                {"role": "system", "content": strict_system},
                {"role": "user", "content": transcript_prompt},
            ],
            "temperature": 0.3,
            "max_completion_tokens": settings.MAX_VERDICT_COMPLETION_TOKENS,
            "reasoning_effort": "low",
            "response_format": {"type": "json_object"},
        }

        try:
            try:
                response = self.client.chat.completions.create(**req_kwargs)
            except (TypeError, APIError):
                req_kwargs.pop("reasoning_effort", None)
                response = self.client.chat.completions.create(**req_kwargs)
        except APIError as e:
            if getattr(e, "status_code", None) == 400:
                raise RuntimeError(
                    "Groq could not generate the jury JSON verdict. "
                    "Try one or two trial rounds with openai/gpt-oss-20b."
                ) from e
            raise

        raw_json = response.choices[0].message.content
        parsed = JuryVerdictSchema.model_validate_json(raw_json)
        resolved_verdict = self._resolve_verdict(parsed)

        badge = (
            "🚨 **GUILTY**"
            if resolved_verdict == "GUILTY"
            else "🛡️ **NOT GUILTY**"
        )
        return (
            f"### ⚖️ Official Supreme Tribunal Verdict: {badge}\n\n"
            f"| Party | Statistical & Evidentiary Score |\n"
            f"| :--- | :--- |\n"
            f"| 🔴 **Opposition Prosecution** | **{parsed.prosecution_score} / 10** |\n"
            f"| 🔵 **Government Defense** | **{parsed.defense_score} / 10** |\n\n"
            f"#### 🔍 Evaluation of Prosecution (Opposition) Evidence\n{parsed.prosecution_analysis}\n\n"
            f"#### 🛡️ Evaluation of Defense (Government) Evidence\n{parsed.defense_analysis}\n\n"
            f"#### 📜 Final Sentence & Sovereign Policy Mandate\n> {parsed.sentence_or_mandate}"
        )