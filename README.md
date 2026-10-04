# Interview Copilot — your AI wingman for job interviews

An always-on voice copilot that listens to your interview and feeds you perfect,
CV-grounded answers in real time.

Built for the **Nebius x NVIDIA Global AI Hackathon** (Personal AI track).

## How it works

1. Click **Start Session** and grant mic access
2. The copilot transcribes the interviewer's speech live (Web Speech API)
3. When it detects a question, **NVIDIA Nemotron** (via Nebius Token Factory)
   generates a concise answer grounded in your CV
4. The answer appears instantly — read it, or have it whispered via TTS
5. Hit **Deep Dive** on tough questions for a detailed STAR-format answer

## Tech

- **LLM:** `nvidia/Nemotron-3_5-Lightning` (real-time answers) +
  `nvidia/nemotron-3-super-120b-a12b` (deep dives) via
  [Nebius Token Factory](https://tokenfactory.nebius.com/) (`NEBIUS_API_KEY`)
- **Backend:** Python FastAPI, OpenAI-compatible client
- **Frontend:** Vite + vanilla JS, Web Speech API (recognition + synthesis)
- **Fallback:** FastRouter (Claude Opus) if Nebius key is absent — dev only

## Quickstart

```bash
# backend
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export NEBIUS_API_KEY=your-key-here
uvicorn app.main:app --port 8771

# frontend (served by backend in prod; dev:)
cd frontend
python -m http.server 8772
# open http://localhost:8772
```

## Layout

- `backend/app/main.py` — FastAPI app, SSE answer streaming
- `backend/app/nemotron.py` — Nebius Token Factory client (OpenAI SDK)
- `backend/app/cv_context.py` — CV grounding context
- `backend/app/questions.py` — question detection heuristics
- `frontend/index.html` — copilot UI

## License

MIT
