# Feedback — Nebius Token Factory & NVIDIA Nemotron

Honest notes from building Interview Copilot (submitted to the Nebius x NVIDIA Global AI Hackathon).

## What worked well
- **OpenAI-compatible API.** Pointing the existing OpenAI client at the Token Factory base URL just worked — zero integration friction.
- **Model catalog.** Finding the exact Nemotron model IDs was straightforward, and both models we used behaved as documented.
- **Nemotron-3.5-Lightning.** Fast and sharp — ideal for the real-time answer path where latency matters more than depth.
- **Nemotron-3-Super-120B.** Excellent at structured STAR-format answers for the deep-dive path.

## Friction
- **Model IDs are case-sensitive** (`nvidia/Nemotron-3_5-Lightning` vs `nvidia/nemotron-3-super-120b-a12b`). We tripped on this once; worth calling out prominently in docs.
- **Thinking by default.** Nemotron 3 "thinks" before answering, which can burn through `max_tokens` on reasoning and return empty content. The `chat_template_kwargs.enable_thinking=false` parameter fixed it, but we only found it after debugging empty responses — this deserves a first-class example in the docs.

## Suggestions
1. A short "migrating from OpenAI" code snippet in the docs (base URL + key swap) would get builders productive in minutes.
2. Document the reasoning/thinking parameters alongside each model card, not just in the API reference.
3. A latency/throughput hint per model in the catalog would help builders pick the right model per use case (we chose Lightning vs Super exactly on this axis).
