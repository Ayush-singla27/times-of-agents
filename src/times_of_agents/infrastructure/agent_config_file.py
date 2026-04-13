from __future__ import annotations

import json
from pathlib import Path

from times_of_agents.domain.entities import AgentConfig, AgentIdentity, EmotionProfile


def load_agent_configs(config_path: Path) -> list[AgentConfig]:
    if not config_path.exists():
        raise FileNotFoundError(f"Agent config file not found: {config_path}")

    with config_path.open("r", encoding="utf-8") as file:
        payload = json.load(file)

    if not isinstance(payload, list):
        raise ValueError("Agent configuration must be a JSON array")

    configs: list[AgentConfig] = []
    for item in payload:
        identity_data = item.get("identity", {})
        emotions_data = item.get("emotion_profile", {})

        identity = AgentIdentity(
            id=str(identity_data["id"]),
            name=str(identity_data["name"]),
            role=str(identity_data["role"]),
            description=str(identity_data["description"]),
        )

        profile = EmotionProfile(
            trust=float(emotions_data["trust"]),
            anticipation=float(emotions_data["anticipation"]),
            joy=float(emotions_data["joy"]),
            surprise=float(emotions_data["surprise"]),
            fear=float(emotions_data["fear"]),
            sadness=float(emotions_data["sadness"]),
            disgust=float(emotions_data["disgust"]),
            anger=float(emotions_data["anger"]),
        )

        configs.append(
            AgentConfig(
                identity=identity,
                emotion_profile=profile,
                speaking_weight=float(item.get("speaking_weight", 1.0)),
            )
        )

    if not configs:
        raise ValueError("At least one agent configuration is required")

    return configs
