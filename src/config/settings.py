import os
from dataclasses import dataclass, field
from typing import List
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class GroqSettings:
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    
    # Your working Groq Models
    AVAILABLE_MODELS: List[str] = field(default_factory=lambda: [
        "openai/gpt-oss-20b",
        "openai/gpt-oss-120b",
        "qwen/qwen3.8-27b",
    ])

    DEFAULT_PROSECUTOR_MODEL: str = "openai/gpt-oss-20b"
    DEFAULT_DEFENSE_MODEL: str = "openai/gpt-oss-20b"
    DEFAULT_JURY_MODEL: str = "openai/gpt-oss-20b"

    MAX_ROUNDS: int = 10
    TEMPERATURE: float = 0.6
    # Keep the request below Groq free-tier models with a 1000-token output limit.
    MAX_COMPLETION_TOKENS: int = 900
    MAX_CONTEXT_CHARS: int = 12000
    MAX_VERDICT_CONTEXT_CHARS: int = 8000
    MAX_VERDICT_COMPLETION_TOKENS: int = 900
    MAX_RETRIES: int = 3

settings = GroqSettings()