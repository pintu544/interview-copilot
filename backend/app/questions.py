"""Question detection heuristics for live interview transcription."""
from __future__ import annotations

import re

QUESTION_WORDS = {
    "what", "why", "how", "when", "where", "which", "who", "whom", "whose",
    "can", "could", "would", "should", "do", "does", "did", "is", "are",
    "was", "were", "have", "has", "had", "will", "tell",
}

# Phrases that almost always introduce a question in interviews.
QUESTION_PHRASES = [
    "tell me about", "walk me through", "describe a time", "give me an example",
    "how do you", "how would you", "what would you", "have you ever",
    "can you explain", "could you explain",
]


def looks_like_question(text: str) -> bool:
    t = text.strip().lower().rstrip(".")
    if not t or len(t.split()) < 3:
        return False
    if "?" in text:
        return True
    if any(t.startswith(p) for p in QUESTION_PHRASES):
        return True
    first = t.split()[0]
    return first in QUESTION_WORDS


def extract_question(transcript: str) -> str | None:
    """Pull the most recent question-like utterance from a transcript chunk."""
    # Split on sentence boundaries; take the last question-like sentence.
    sentences = re.split(r"(?<=[.?!])\s+", transcript.strip())
    for s in reversed(sentences):
        if looks_like_question(s):
            return s.strip()
    return None
