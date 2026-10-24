import gradio as gr

from src.ui.gradio_app import COURTROOM_CSS, create_gradio_app

# Dark-tuned Soft theme so inputs, tabs, and markdown never clash with light mode
courtroom_theme = gr.themes.Soft(
    primary_hue="amber",
    secondary_hue="slate",
    neutral_hue="slate",
).set(
    body_background_fill="#090a0f",
    body_background_fill_dark="#090a0f",
    block_background_fill="#12151f",
    block_background_fill_dark="#12151f",
    block_border_color="#2a2f42",
    block_border_color_dark="#2a2f42",
    input_background_fill="#1a1f2e",
    input_background_fill_dark="#1a1f2e",
    body_text_color="#f4f1ea",
    body_text_color_dark="#f4f1ea",
)

if __name__ == "__main__":
    app = create_gradio_app()
    app.queue()  # Enables non-blocking concurrent generator streaming
    app.launch(
        server_name="127.0.0.1",
        server_port=7860,
        share=False,
        theme=courtroom_theme,
        css=COURTROOM_CSS,
    )