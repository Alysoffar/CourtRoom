import gradio as gr

from src.config.settings import settings
from src.domain.enums import AgentRole
from src.services.llm_provider import GroqCourtroomProvider
from src.services.orchestrator import CourtroomOrchestrator
from src.services.tts_provider import LocalSpeechProvider

PRESET_CRIMES = [
    "Misappropriation of $4.2B in Sovereign Green Energy & Infrastructure Funds",
    "Unconstitutional Surveillance of Journalists & Political Dissidents",
    "Central Bank Manipulation & Artificial Currency Devaluation",
    "Negligence Leading to National Power Grid & Water Supply Collapse",
    "Illegal Resource Extraction & Environmental Destruction in Protected Zones",
    "Custom Indictment (Type below)",
]

COURTROOM_CSS = """
:root { --ink: #f5f0e8; --muted: #a9a39a; --gold: #d8ad60; --panel: #171a21; }
.gradio-container { max-width: 1480px !important; background: #0b0d12 !important; color: var(--ink); }
.hero { padding: 28px 34px; border: 1px solid #403728; border-radius: 22px;
    background: radial-gradient(circle at 72% 12%, #49391f 0, #1c1d24 42%, #101117 100%);
    box-shadow: 0 18px 60px #0008; margin-bottom: 18px; }
.hero h1 { margin: 0; color: #f3d38a; font-size: 38px; letter-spacing: 2px; }
.hero p { color: #c7c0b5; font-size: 16px; margin: 8px 0 0; }
.scene { min-height: 215px; padding: 18px; border: 1px solid #55452d; border-radius: 18px;
    background: linear-gradient(180deg, #2b2119 0%, #17151a 62%, #0e1016 63%); position: relative;
    overflow: hidden; text-align: center; }
.scene:before { content: "JUSTICE"; position: absolute; inset: 24px 0 auto; color: #ead18d;
    font: 700 22px Georgia; letter-spacing: 10px; opacity: .65; }
.bench { position: absolute; left: 18%; right: 18%; bottom: 28px; height: 35px;
    background: linear-gradient(#8e6236, #482c1a); border: 2px solid #c18c4d; border-radius: 8px; }
.avatar { position: absolute; bottom: 55px; width: 112px; height: 112px; border-radius: 50%;
    border: 3px solid; display: flex; flex-direction: column; justify-content: center;
    align-items: center; font-size: 40px; box-shadow: 0 0 35px #0008; }
.avatar span { font: 700 11px Arial; letter-spacing: 1px; margin-top: 3px; }
.judge { left: calc(50% - 56px); background: #283852; border-color: #84a7d7; }
.pros { left: 6%; background: #54272b; border-color: #e2746e; }
.def { right: 6%; background: #273c3a; border-color: #70c4a5; }
.section-title { color: #e4bd6d; letter-spacing: 1px; font-weight: 700; }
.status-card { border: 1px solid #383b46; border-radius: 14px; padding: 12px 16px; background: #14161d; }
.gradio-chatbot { border: 1px solid #383b46 !important; border-radius: 16px !important; }
.round-card { border: 1px solid #51442d; border-radius: 14px; background: #14161d; padding: 10px; }
"""


def create_gradio_app() -> gr.Blocks:
    speech = LocalSpeechProvider()

    with gr.Blocks(title="The Sovereign Tribunal") as app:
        gr.HTML(
            """
            <div class="hero">
                <h1>⚖ THE SOVEREIGN TRIBUNAL</h1>
                <p>Build your case. Challenge the chamber. Let the evidence speak.</p>
            </div>
            """
        )

        with gr.Row():
            with gr.Column(scale=1, min_width=310):
                gr.Markdown("### 📁 CASE FILE", elem_classes="section-title")
                country_input = gr.Dropdown(
                    choices=["Egypt", "Brazil", "Germany", "Japan", "United Kingdom", "United States"],
                    value="Egypt",
                    allow_custom_value=True,
                    label="Jurisdiction",
                    info="Choose a country or type your own.",
                )
                crime_dropdown = gr.Dropdown(
                    choices=PRESET_CRIMES,
                    value=PRESET_CRIMES[0],
                    label="Indictment",
                )
                custom_crime_input = gr.Textbox(
                    label="Custom indictment",
                    placeholder="Describe the accusation...",
                    visible=False,
                )
                rounds_slider = gr.Slider(
                    minimum=1, maximum=settings.MAX_ROUNDS, value=3, step=1,
                    label="Trial rounds",
                )
                gr.Markdown("### 🎭 CAST & AUDIO", elem_classes="section-title")
                pros_model_dd = gr.Dropdown(
                    choices=settings.AVAILABLE_MODELS,
                    value=settings.DEFAULT_PROSECUTOR_MODEL,
                    label="Opposition Prosecutor",
                )
                def_model_dd = gr.Dropdown(
                    choices=settings.AVAILABLE_MODELS,
                    value=settings.DEFAULT_DEFENSE_MODEL,
                    label="Government Defense",
                )
                jury_model_dd = gr.Dropdown(
                    choices=settings.AVAILABLE_MODELS,
                    value=settings.DEFAULT_JURY_MODEL,
                    label="Supreme Jury",
                )
                auto_tts = gr.Checkbox(
                    value=True,
                    label="🔊 Speak new arguments automatically",
                )
                with gr.Row():
                    start_btn = gr.Button("⚔ CONVENE COURT", variant="primary")
                    replay_btn = gr.Button("▶ REPLAY", variant="secondary")
                audio_output = gr.Audio(
                    label="Courtroom voice",
                    type="filepath",
                    autoplay=True,
                )
                latest_statement = gr.State("")

            with gr.Column(scale=2, min_width=620):
                gr.HTML(
                    """
                    <div class="scene">
                        <div class="avatar pros">🔴<span>PROSECUTION</span></div>
                        <div class="avatar judge">⚖<span>THE JURY</span></div>
                        <div class="avatar def">🔵<span>DEFENSE</span></div>
                        <div class="bench"></div>
                    </div>
                    """
                )
                status_box = gr.Markdown(
                    "🟡 **Chambers quiet.** File an indictment to begin.",
                    elem_classes="status-card",
                )
                gr.Markdown("### 🎙 LIVE TRANSCRIPT", elem_classes="section-title")
                chatbot = gr.Chatbot(
                    label="Courtroom transcript",
                    height=480,
                    layout="bubble",
                    show_label=False,
                )
                gr.Markdown("### 🏛 JURY DELIBERATION", elem_classes="section-title")
                verdict_box = gr.Markdown("*The jury is waiting for the evidence...*")
                gr.Markdown("### 🗂 EVIDENCE LOCKER", elem_classes="section-title")
                evidence_box = gr.Markdown("*No exhibits logged yet...*")

        crime_dropdown.change(
            fn=lambda crime: gr.update(
                visible=(crime == "Custom Indictment (Type below)")
            ),
            inputs=crime_dropdown,
            outputs=custom_crime_input,
        )

        def run_groq_session(
            country: str,
            preset_crime: str,
            custom_crime: str,
            rounds: int,
            pros_model: str,
            def_model: str,
            jury_model: str,
            speak_automatically: bool,
        ):
            effective_key = settings.GROQ_API_KEY.strip()
            if not effective_key:
                raise gr.Error("Set GROQ_API_KEY in the .env file before convening court.")
            if not country or not country.strip():
                raise gr.Error("Specify a target country.")

            selected_crime = (
                custom_crime.strip()
                if preset_crime == "Custom Indictment (Type below)"
                else preset_crime
            )
            if not selected_crime:
                raise gr.Error("Specify the crime or indictment.")

            provider = GroqCourtroomProvider(api_key=effective_key)
            orchestrator = CourtroomOrchestrator(llm_provider=provider)
            last_statement = ""
            spoken_turn_key = None
            spoken_statement = None

            for case_state, evidence_md in orchestrator.run_trial(
                country=country.strip(),
                crime=selected_crime,
                num_rounds=int(rounds),
                prosecutor_model=pros_model,
                defense_model=def_model,
                jury_model=jury_model,
            ):
                chat_messages = []
                for turn in case_state.transcript:
                    is_pros = turn.role == AgentRole.PROSECUTION
                    badge = "🔴" if is_pros else "🔵"
                    chat_messages.append(
                        {
                            "role": "user" if is_pros else "assistant",
                            "content": (
                                f"{badge} **{turn.role.value} · Round "
                                f"{turn.round_number}**\n\n{turn.statement}"
                            ),
                        }
                    )

                current_turn = case_state.transcript[-1]
                current_turn_key = (
                    current_turn.round_number,
                    current_turn.role,
                )
                audio_path = None
                if (
                    speak_automatically
                    and last_statement
                    and current_turn_key != spoken_turn_key
                ):
                    audio_path = speech.synthesize(last_statement)
                    spoken_turn_key = current_turn_key
                    spoken_statement = last_statement

                completed_turn = current_turn
                last_statement = completed_turn.statement
                if (
                    case_state.verdict_report
                    and speak_automatically
                    and last_statement != spoken_statement
                ):
                    audio_path = speech.synthesize(last_statement)
                    spoken_statement = last_statement
                verdict_md = (
                    case_state.verdict_report
                    or f"*Round {completed_turn.round_number} in progress · "
                    f"{len(case_state.transcript)}/{case_state.max_rounds * 2} arguments*"
                )
                status = (
                    f"🟢 **Round {completed_turn.round_number} · "
                    f"{completed_turn.role.value} has the floor**"
                )
                yield (
                    chat_messages,
                    evidence_md,
                    verdict_md,
                    status,
                    audio_path,
                    last_statement,
                )

        start_btn.click(
            fn=run_groq_session,
            inputs=[
                country_input,
                crime_dropdown,
                custom_crime_input,
                rounds_slider,
                pros_model_dd,
                def_model_dd,
                jury_model_dd,
                auto_tts,
            ],
            outputs=[
                chatbot,
                evidence_box,
                verdict_box,
                status_box,
                audio_output,
                latest_statement,
            ],
        )

        replay_btn.click(
            fn=speech.synthesize,
            inputs=latest_statement,
            outputs=audio_output,
        )

    return app
