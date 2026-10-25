import uvicorn

from src.api.application import create_app

app = create_app()


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=7860, reload=True)
