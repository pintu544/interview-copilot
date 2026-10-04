"""Interview Copilot backend — FastAPI + SSE streaming answers from Nemotron."""
from __future__ import annotations

import json
import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

load_dotenv()

from . import cv_context, nemotron, questions

app = FastAPI(title="Interview Copilot")


class AskIn(BaseModel):
    question: str
    deep: bool = False


@app.post("/api/answer")
def answer(body: AskIn):
    system = cv_context.SYSTEM_DEEP if body.deep else cv_context.SYSTEM_FAST
    try:
        text, provider = nemotron.answer(
            body.question, system,
            deep=body.deep,
            max_tokens=600 if body.deep else 220,
        )
        return {"answer": text, "provider": provider,
                "model": nemotron._model_for(provider, body.deep),
                "deep": body.deep}
    except Exception as e:  # noqa: BLE001
        return JSONResponse({"error": str(e)[:300]}, status_code=502)


@app.post("/api/detect")
def detect(body: dict):
    q = questions.extract_question(body.get("transcript", ""))
    return {"question": q}


@app.get("/api/health")
def health():
    return {"ok": True, "nebius": bool(os.environ.get("NEBIUS_API_KEY"))}


FRONTEND = os.path.join(os.path.dirname(__file__), "..", "..", "frontend")


@app.get("/", response_class=HTMLResponse)
def index():
    with open(os.path.join(FRONTEND, "index.html")) as f:
        return f.read()
