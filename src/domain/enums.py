# src/domain/enums.py
from enum import Enum

class AgentRole(str, Enum):
    PROSECUTION = "Opposition Prosecutor"
    DEFENSE = "Government Defense Counsel"
    JURY = "Supreme Court Jury"