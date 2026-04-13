from __future__ import annotations

from agentpress_backend.domain.entities import AgentConfig


def build_system_prompt(agent_config: AgentConfig) -> str:
    emotions = agent_config.emotion_profile.to_dict()
    dominant = agent_config.emotion_profile.dominant_emotion()
    emotion_str = ", ".join(f"{key}: {value:.2f}" for key, value in emotions.items())

    return (
        f"You are {agent_config.identity.name}, a {agent_config.identity.role}.\n\n"
        f"Role Description: {agent_config.identity.description}\n\n"
        f"Your Emotional Disposition (Plutchik Profile):\n{emotion_str}\n\n"
        f"Dominant Emotion: {dominant.upper()}\n\n"
        "Your task is to engage in a thoughtful, nuanced, multi-agent discussion about a given news topic. "
        "When prior statements exist, treat them as comments from peers and actively respond to them.\n"
        "Writing rules:\n"
        "1. Ground analysis in your emotional and analytical disposition.\n"
        "2. If prior context is present, reference at least one peer statement and either support, refine, or challenge it.\n"
        "3. Add one concrete implication, recommendation, or unresolved question.\n"
        "4. Mention confidence level briefly (high/medium/low + short reason).\n"
        "5. Do not start every sentence by repeating your role or identity. Mention your role at most once, only if relevant.\n\n"
        f"Remember: You approach topics with a dominant lens of {dominant}. "
        "Be authentic to this perspective while remaining intellectually honest."
    )