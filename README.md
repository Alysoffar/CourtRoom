# CourtRoom AI

CourtRoom AI is an interactive, game-style political and criminal tribunal built with Python, FastAPI, Groq, and local text-to-speech.

Users choose a jurisdiction and indictment, then watch an AI prosecution and AI defense present evidence in a streamed courtroom transcript. A jury model evaluates the debate and produces a structured verdict.

## Features

- Country selection with support for custom jurisdictions
- Suggested indictments and custom indictment entry
- Opposition prosecutor and government defense agents
- Configurable trial length with a maximum of 10 rounds
- Live streaming courtroom transcript
- Evidence locker that extracts exhibits from arguments
- Structured jury verdict with prosecution and defense scores
- Courtroom-themed Three.js and Tailwind browser interface
- Animated characters for the prosecution, jury, and defense
- Optional automatic speech playback for the final verdict
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
    ├── api/
    │   ├── application.py
    │   └── routes/
    │       ├── static.py
    │       ├── trial.py
    │       └── tts.py
    ├── config/
    │   ├── settings.py
    │   └── trial_options.py
    ├── domain/
    ├── prompts/
    ├── services/
    └── ui/
        ├── courtroom.html
        └── static/
            ├── app.js
            └── styles.css
```

## Requirements

- Python 3.10 or newer
- A Groq API key
- Windows Speech API support for local text-to-speech
- A modern browser with WebSocket and WebGL support

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

Text-to-speech uses `pyttsx3` and the locally installed Windows speech engine. Enable **Auto-TTS Verdict** to hear the final verdict automatically, or use **TTS** to replay the latest statement.

If speech synthesis is unavailable, install the project requirements again and confirm that Windows has at least one installed speech voice.

## Groq model and token usage

The application defaults to:

- `openai/gpt-oss-20b` for the prosecutor
- `openai/gpt-oss-20b` for the defense
- `openai/gpt-oss-20b` for the jury

The model list is configured in `src/config/settings.py`, and available models can vary by Groq account. The application requests a maximum of 900 completion tokens to remain below common free-tier output limits. If Groq reports a `429` or `413` error, wait for the quota window to reset, reduce the number of trial rounds, or select a model available to your account.

## API surface

- `GET /` serves the courtroom web interface.
- `GET /api/config` returns available models, preset indictments, and UI limits.
- `POST /api/tts` synthesizes a local WAV file from text.
- `WebSocket /ws/trial` streams courtroom arguments, evidence, and the final verdict.

The browser assets are served from `/static`. The FastAPI application is assembled in `src/api/application.py`, while each route group has its own module under `src/api/routes/`.

## Security

- Store API keys only in `.env`.
- Do not commit `.env`.
- If an API key is exposed, revoke it immediately in the Groq console and create a replacement.
- AI-generated arguments may contain inaccurate claims. Treat courtroom statements as fictional analysis, not legal advice or verified reporting.

## Development checks

Compile the application modules to check syntax:

```powershell
python -m py_compile main.py src\api\application.py src\api\routes\static.py src\api\routes\tts.py src\api\routes\trial.py src\config\settings.py src\config\trial_options.py src\services\llm_provider.py src\services\orchestrator.py src\services\tts_provider.py
```