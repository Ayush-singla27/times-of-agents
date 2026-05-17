from __future__ import annotations

from crewai import LLM


def _has_provider_prefix(model: str) -> bool:
    known_prefixes = {
        "anthropic",
        "azure",
        "bedrock",
        "cohere",
        "google",
        "groq",
        "mistral",
        "ollama",
        "openai",
    }
    provider, _, _ = model.partition("/")
    return provider in known_prefixes


def create_crewai_llm(model: str, temperature: float = 0.7) -> LLM:
    prefixed = model if _has_provider_prefix(model) else f"openai/{model}"
    return LLM(model=prefixed, temperature=temperature)
