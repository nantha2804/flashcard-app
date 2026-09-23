from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.openai_client import generate_flashcards

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")

@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(request, "index.html", {"request": request})

@app.post("/generate", response_class=HTMLResponse)
def generate(request: Request, topic: str = Form(...)):
    cards = generate_flashcards(topic)
    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "request": request,
            "cards": cards,
            "topic": topic,
        },
    )