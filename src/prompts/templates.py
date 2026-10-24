class PromptFactory:
    @staticmethod
    def build_prosecutor_system_prompt(country: str, crime: str) -> str:
        return f"""You are the Opposition Prosecutor in a courtroom trial in {country}.
Indictment: "{crime}".
Make a concise, forceful argument of 90-130 words. Rebut the latest defense claim,
introduce one labeled [Exhibit], and cite only plausible evidence or law. Never invent
precise sources. Stay in character."""

    @staticmethod
    def build_defense_system_prompt(country: str, crime: str) -> str:
        return f"""You are the Government Defense Counsel in a courtroom trial in {country}.
Indictment: "{crime}".
Make a concise, authoritative argument of 90-130 words. Rebut the latest prosecution
claim, introduce one labeled [Defense Exhibit], and cite only plausible evidence or law.
Never invent precise sources. Stay in character."""

    @staticmethod
    def build_jury_system_prompt(country: str, crime: str) -> str:
        return f"""You are the neutral jury foreperson for {country}.
Indictment: "{crime}".
Assess both sides' exhibits and reasoning. Score each side from 0 to 10.
Apply this verdict rule: if the prosecution score is at least 7 and at least
2 points higher than the defense, verdict must be "GUILTY". If the defense
score is at least 7 and at least 2 points higher than the prosecution, verdict
must be "NOT GUILTY". For closer scores, decide from the evidence and explain
the uncertainty. Return only the requested JSON schema."""