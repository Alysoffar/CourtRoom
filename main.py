import gradio as gr

from src.ui.gradio_app import COURTROOM_CSS, create_gradio_app

if __name__ == "__main__":
    app = create_gradio_app()
    app.queue()  # Enables non-blocking concurrent generator streaming
    app.launch(
        server_name="127.0.0.1",
        server_port=7860,
        share=False,
        theme=gr.themes.Soft(),
        css=COURTROOM_CSS,
    )