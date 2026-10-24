import gradio as gr

from src.config.settings import settings
from src.domain.enums import AgentRole
from src.services.llm_provider import GroqCourtroomProvider
from src.services.orchestrator import CourtroomOrchestrator
from src.ui.courtroom_scene import render_3d_courtroom
from src.ui.theme import COURTROOM_CSS

PRESET_CRIMES = [
    "Misappropriation of $4.2B in Sovereign Green Energy & Infrastructure Funds",
    "Unconstitutional Surveillance of Journalists & Political Dissidents",
    "Central Bank Manipulation & Artificial Currency Devaluation",
    "Negligence Leading to National Power Grid & Water Supply Collapse",
    "Illegal Resource Extraction & Environmental Destruction in Protected Zones",
    "Custom Indictment (Type below)",
]


def create_gradio_app() -> gr.Blocks:
    # In Gradio 5, css and theme are passed to app.launch() in main.py
    with gr.Blocks(title="The Sovereign Tribunal") as app:
        gr.HTML(
            """
            <div class="tribunal-header">
                <div>
                    <h1>⚖ THE SOVEREIGN TRIBUNAL</h1>
                    <p>3D Interactive AI Courtroom · Prosecution vs. Government Defense · Supreme Jury Deliberation</p>
                </div>
                <div class="header-badge">CHAMBER SESSION ACTIVE</div>
            </div>
            """
        )

        with gr.Row():
            # ================= LEFT COLUMN: CONTROLS =================
            with gr.Column(scale=1, min_width=320, elem_classes="control-card"):
                gr.Markdown("### 📁 CASE DOCKET", elem_classes="section-title")
                country_input = gr.Dropdown(
                    choices=["Egypt", "Brazil", "Germany", "Japan", "United Kingdom", "United States"],
                    value="Egypt",
                    allow_custom_value=True,
                    label="Jurisdiction",
                    info="Select a nation or type a custom jurisdiction.",
                )
                crime_dropdown = gr.Dropdown(
                    choices=PRESET_CRIMES,
                    value=PRESET_CRIMES[0],
                    label="Bill of Indictment",
                )
                custom_crime_input = gr.Textbox(
                    label="Custom Indictment",
                    placeholder="Enter specific constitutional or criminal charges...",
                    visible=False,
                    lines=2,
                )
                rounds_slider = gr.Slider(
                    minimum=1,
                    maximum=settings.MAX_ROUNDS,
                    value=3,
                    step=1,
                    label="Trial Rounds",
                )

                gr.Markdown("### 🎭 CHIBI CAST & MODELS", elem_classes="section-title")
                pros_model_dd = gr.Dropdown(
                    choices=settings.AVAILABLE_MODELS,
                    value=settings.DEFAULT_PROSECUTOR_MODEL,
                    label="🔴 Opposition Prosecutor",
                )
                def_model_dd = gr.Dropdown(
                    choices=settings.AVAILABLE_MODELS,
                    value=settings.DEFAULT_DEFENSE_MODEL,
                    label="🔵 Government Defense",
                )
                jury_model_dd = gr.Dropdown(
                    choices=settings.AVAILABLE_MODELS,
                    value=settings.DEFAULT_JURY_MODEL,
                    label="⚖️ Supreme Jury",
                )

                start_btn = gr.Button("⚔ CONVENE COURT", variant="primary")

            # ================= RIGHT COLUMN: 3D STAGE & RECORDS =================
            with gr.Column(scale=3, min_width=680):
                courtroom_stage = gr.HTML(
                    value=render_3d_courtroom(
                        country="Egypt",
                        pros_model=settings.DEFAULT_PROSECUTOR_MODEL,
                        def_model=settings.DEFAULT_DEFENSE_MODEL,
                        jury_model=settings.DEFAULT_JURY_MODEL,
                    )
                )

                with gr.Tabs():
                    with gr.TabItem("🎙 Full Courtroom Transcript"):
                        chatbot = gr.Chatbot(
                            label="Courtroom Transcript",
                            height=360,
                            show_label=False,
                            group_consecutive_messages=False,
                            autoscroll=False,
                        )
                    with gr.TabItem("🏛 Supreme Jury Verdict & Scores"):
                        verdict_box = gr.Markdown(
                            "*The Supreme Jury is seated and waiting for arguments to conclude...*"
                        )
                    with gr.TabItem("🗂 Evidence Locker"):
                        evidence_box = gr.Markdown(
                            "*Exhibits cited by the Prosecution and Defense will be logged here automatically...*"
                        )

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
                    if not turn.statement or not turn.statement.strip():
                        continue
                    is_pros = turn.role == AgentRole.PROSECUTION
                    badge = "🔴" if is_pros else "🔵"
                    chat_messages.append(
                        {
                            "role": "user" if is_pros else "assistant",
                            "content": (
                                f"{badge} **{turn.role.value} · Round "
                                f"{turn.round_number}**\n\n{turn.statement.strip()}"
                            ),
                        }
                    )

                current_turn = case_state.transcript[-1]
                if case_state.verdict_report:
                    active_role = "JURY"
                    speaker_title = "SUPREME JURY · FINAL VERDICT"
                    round_label = "VERDICT DELIVERED"
                    vn_text = case_state.verdict_report
                else:
                    is_pros_turn = current_turn.role == AgentRole.PROSECUTION
                    active_role = "PROSECUTION" if is_pros_turn else "DEFENSE"
                    speaker_title = (
                        "OPPOSITION PROSECUTOR" if is_pros_turn else "GOVERNMENT DEFENSE"
                    )
                    round_label = f"ROUND {current_turn.round_number} OF {case_state.max_rounds}"
                    vn_text = (
                        current_turn.statement
                        or f"Preparing arguments for Round {current_turn.round_number}..."
                    )

                stage_html = render_3d_courtroom(
                    active_role=active_role,
                    speaker_title=speaker_title,
                    dialogue_text=vn_text,
                    round_label=round_label,
                    country=country.strip(),
                    pros_model=pros_model,
                    def_model=def_model,
                    jury_model=jury_model,
                )

                visible_turns = len(chat_messages)
                verdict_md = (
                    case_state.verdict_report
                    or f"*⏳ Trial in session (Round {current_turn.round_number}/{case_state.max_rounds}) · "
                    f"{visible_turns}/{case_state.max_rounds * 2} statements recorded. "
                    f"Switch to the Supreme Jury tab once deliberation concludes.*"
                )

                yield (
                    stage_html,
                    chat_messages,
                    evidence_md or "*No exhibits logged yet...*",
                    verdict_md,
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
            ],
            outputs=[
                courtroom_stage,
                chatbot,
                evidence_box,
                verdict_box,
            ],
        )

    return app
