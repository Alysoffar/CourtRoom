import json
from typing import List, Dict, Generator
from groq import Groq, RateLimitError, APIError
from src.config.settings import settings
from src.domain.schemas import JuryVerdictSchema

class GroqCourtroomProvider:
    def __init__(self, api_key: str):
        self.client = Groq(
            api_key=api_key,
            max_retries=settings.MAX_RETRIES,  # Native exponential backoff for free-tier RPM limits
        )

    def stream_turn(
        self, model: str, system_prompt: str, messages: List[Dict[str, str]]
    ) -> Generator[str, None, None]:
        """Streams tokens in real-time from Groq's LPU."""
        payload = [{"role": "system", "content": system_prompt}] + messages
        try:
            stream = self.client.chat.completions.create(
                model=model,
                messages=payload,
                temperature=settings.TEMPERATURE,
                max_completion_tokens=settings.MAX_COMPLETION_TOKENS,
                stream=True,
            )
            partial_text = ""
            for chunk in stream:
                delta = chunk.choices[0].delta.content
                if delta:
                    partial_text += delta
                    yield partial_text
        except RateLimitError as e:
            raise RuntimeError(f"Groq Free Tier Rate Limit reached. Please wait a few seconds: {e}")
        except APIError as e:
            if getattr(e, "status_code", None) == 413:
                raise RuntimeError(
                    "This courtroom request exceeded Groq's free-tier token limit. "
                    "Use fewer trial rounds or the lighter openai/gpt-oss-20b model."
                ) from e
            raise RuntimeError(f"Groq API Error: {e}")

    def generate_structured_verdict(
        self, model: str, system_prompt: str, transcript_prompt: str
    ) -> str:
        """Uses Groq's JSON mode + Pydantic validation to generate an air-tight Jury Verdict."""
        schema_json = json.dumps(JuryVerdictSchema.model_json_schema(), indent=2)
        strict_system = (
            f"{system_prompt}\n\n"
            f"You MUST respond ONLY with a valid JSON object matching this exact schema:\n{schema_json}"
        )

        response = self.client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": strict_system},
                {"role": "user", "content": transcript_prompt},
            ],
            temperature=0.3,
            max_completion_tokens=settings.MAX_VERDICT_COMPLETION_TOKENS,
            response_format={"type": "json_object"},
        )

        raw_json = response.choices[0].message.content
        parsed = JuryVerdictSchema.model_validate_json(raw_json)

        badge = "🚨 **GUILTY**" if "GUILTY" in parsed.verdict.upper() and "NOT" not in parsed.verdict.upper() else "🛡️ **NOT GUILTY**"
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