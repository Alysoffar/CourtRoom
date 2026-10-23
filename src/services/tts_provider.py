from pathlib import Path
from tempfile import NamedTemporaryFile

import pyttsx3


class LocalSpeechProvider:
    def __init__(self) -> None:
        self.engine = pyttsx3.init()

    def synthesize(self, text: str) -> str:
        clean_text = text.strip()
        if not clean_text:
            raise ValueError("Cannot synthesize empty courtroom text.")

        with NamedTemporaryFile(suffix=".wav", delete=False) as audio_file:
            output_path = Path(audio_file.name)

        try:
            self.engine.save_to_file(clean_text, str(output_path))
            self.engine.runAndWait()
        except Exception as exc:
            output_path.unlink(missing_ok=True)
            raise RuntimeError(f"Local text-to-speech failed: {exc}") from exc

        return str(output_path)
