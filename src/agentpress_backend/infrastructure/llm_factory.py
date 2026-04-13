from __future__ import annotations

from crewai import LLM


def create_crewai_llm(model: str, temperature: float = 0.7) -> LLM:
    prefixed = model if model.startswith("anthropic/") else f"anthropic/{model}"
    return LLM(model=prefixed, temperature=temperature)
