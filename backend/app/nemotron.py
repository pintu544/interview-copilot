"""Nebius Token Factory client — OpenAI-compatible, NVIDIA Nemotron models.

Model IDs are case-sensitive (exact strings from the Nebius catalog).
Nemotron 3 "thinks" by default; we disable thinking for direct output.
Falls back to FastRouter (Claude) when NEBIUS_API_KEY is absent (dev only).
"""
from __future__ import annotations

import logging
import os

log = logging.getLogger("copilot.nemotron")

BASE_URL = "https://api.tokenfactory.nebius.com/v1/"

# Exact model IDs from the Nebius public catalog (case-sensitive).
MODEL_FAST = "nvidia/Nemotron-3_5-Lightning"      # 30B MoE — real-time answers
MODEL_DEEP = "nvidia/nemotron-3-super-120b-a12b"  # 120B MoE — deep dives

_client = None
_provider = None


def _get_client():
    global _client, _provider
    if _client is not None:
        return _client, _provider
    from openai import OpenAI

    nebius_key = os.environ.get("NEBIUS_API_KEY")
    if nebius_key:
        _client = OpenAI(base_url=BASE_URL, api_key=nebius_key)
        _provider = "nebius"
        log.info("Nemotron client active (Nebius Token Factory)")
    else:
        fr_key = os.environ.get("LLM_API_KEY")
        if not fr_key:
            raise RuntimeError("Set NEBIUS_API_KEY (or LLM_API_KEY for dev fallback)")
        _client = OpenAI(
            base_url=os.environ.get("LLM_BASE_URL", "https://api.fastrouter.ai/v1"),
            api_key=fr_key,
        )
        _provider = "fastrouter"
        log.warning("NEBIUS_API_KEY absent — using FastRouter fallback (dev only)")
    return _client, _provider


def _model_for(provider: str, deep: bool) -> str:
    if provider == "nebius":
        return MODEL_DEEP if deep else MODEL_FAST
    return os.environ.get("LLM_MODEL", "anthropic/claude-opus-4-7")


def answer(question: str, system: str, deep: bool = False,
           max_tokens: int = 300) -> tuple[str, str]:
    """Return (answer_text, provider)."""
    client, provider = _get_client()
    kwargs: dict = {
        "model": _model_for(provider, deep),
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": question},
        ],
        "max_tokens": max_tokens,
        "temperature": 0.7,
    }
    # Nemotron 3 thinks by default and can burn max_tokens on reasoning;
    # disable for direct-output calls (Nebius-only param).
    if provider == "nebius":
        kwargs["extra_body"] = {
            "chat_template_kwargs": {"enable_thinking": False}
        }
    resp = client.chat.completions.create(**kwargs)
    text = (resp.choices[0].message.content or "").strip()
    # If thinking wasn't disabled server-side, content may be empty with
    # reasoning in reasoning_content — surface a graceful fallback.
    if not text:
        text = "(The model returned only reasoning tokens — try Deep Dive.)"
    return text, provider
