# CourtRoom AI

CourtRoom AI is an interactive, game-style political and criminal tribunal built with Python, Gradio, Groq, and local text-to-speech.

Users choose a jurisdiction and indictment, then watch an AI prosecution and AI defense present evidence in a streamed courtroom transcript. A jury model evaluates the debate and produces a structured verdict.

## Features

- Country selection with support for custom jurisdictions
- Suggested indictments and custom indictment entry
- Opposition prosecutor and government defense agents
- Configurable trial length with a maximum of 10 rounds
- Live streaming courtroom transcript
- Evidence locker that extracts exhibits from arguments
- Structured jury verdict with prosecution and defense scores
- Courtroom-themed Gradio interface
- Character placeholders for the prosecution, jury, and defense
- Optional automatic speech playback for new arguments
- Manual replay using local Windows text-to-speech
- Context and completion limits designed for Groq free-tier token limits

## Project structure

```text
CourtRoom/
├── .env.example
├── main.py
├── README.md
├── requirements.txt
└── src/
    ├── config/
    ├── domain/
    ├── prompts/
    ├── services/
    └── ui/
```

## Requirements

- Python 3.10 or newer
- A Groq API key
- Windows Speech API support for local text-to-speech

## Setup

Open PowerShell in the project directory:

```powershell
cd "D:\college work\Term7\Prof_training\CourtRoom"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Create a local `.env` file from the example:

```powershell
Copy-Item .env.example .env
```

Set the Groq key in `.env`:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Never commit `.env` or share its API key. The file is excluded by `.gitignore`.

## Run the application

```powershell
.\.venv\Scripts\Activate.ps1
python main.py
```

Open the local URL in a browser:

```text
http://127.0.0.1:7860
```

Keep the terminal running while using the application. Press `Ctrl+C` to stop the server.

## Text-to-speech

Text-to-speech uses `pyttsx3` and the locally installed Windows speech engine. Enable **Speak new arguments automatically** to hear new arguments as they finish, or use **Replay** to hear the latest statement again.

If speech synthesis is unavailable, install the project requirements again and confirm that Windows has at least one installed speech voice.

## Groq model and token usage

The application defaults to:

- `openai/gpt-oss-20b` for the prosecutor
- `openai/gpt-oss-20b` for the defense
- `openai/gpt-oss-20b` for the jury

The model list is configured in `src/config/settings.py`. Available models can vary by Groq account. If Groq reports a `413` token-limit error, reduce the number of trial rounds and use `openai/gpt-oss-20b`.

## Security

- Store API keys only in `.env`.
- Do not commit `.env`.
- If an API key is exposed, revoke it immediately in the Groq console and create a replacement.
- AI-generated arguments may contain inaccurate claims. Treat courtroom statements as fictional analysis, not legal advice or verified reporting.

## Development checks

Compile the main modules to check syntax:

```powershell
python -m py_compile main.py src\ui\gradio_app.py src\services\tts_provider.py
```