from dataclasses import dataclass, field
from typing import List, Optional
from pydantic import BaseModel, Field
from src.domain.enums import AgentRole

class JuryVerdictSchema(BaseModel):
    prosecution_score: int = Field(description="Score out of 10 for Prosecution's statistical rigor and legal evidence")
    defense_score: int = Field(description="Score out of 10 for Defense's statistical rigor and legal counter-evidence")
    prosecution_analysis: str = Field(description="Critique of the Opposition Prosecutor's exhibits and statistics")
    defense_analysis: str = Field(description="Critique of the Government Defense's counter-exhibits and statistics")
    verdict: str = Field(description="Strictly 'GUILTY' or 'NOT GUILTY'")
    sentence_or_mandate: str = Field(description="Final sentence, sanctions, or constitutional policy mandate")

@dataclass
class CourtTurn:
    round_number: int
    role: AgentRole
    model_used: str
    statement: str

@dataclass
class CaseFile:
    country: str
    crime: str
    max_rounds: int
    transcript: List[CourtTurn] = field(default_factory=list)
    verdict_report: Optional[str] = None