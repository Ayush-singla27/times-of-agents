from __future__ import annotations

import json

import pytest

from times_of_agents.infrastructure.agent_config_file import load_agent_configs


def _base_agent_payload() -> dict[str, object]:
    return {
        "identity": {
            "id": "a1",
            "name": "Agent 1",
            "role": "Analyst",
            "description": "Testing",
        },
        "emotion_profile": {
            "trust": 0.5,
            "anticipation": 0.5,
            "joy": 0.5,
            "surprise": 0.5,
            "fear": 0.5,
            "sadness": 0.5,
            "disgust": 0.5,
            "anger": 0.5,
        },
    }


def test_load_agent_config_defaults_for_memory_fields(tmp_path) -> None:
    config_path = tmp_path / "agents.json"
    config_path.write_text(json.dumps([_base_agent_payload()]), encoding="utf-8")

    configs = load_agent_configs(config_path)

    assert len(configs) == 1
    assert configs[0].memory_window_messages == 8
    assert configs[0].include_topic_every_turn is True
    assert configs[0].temperature == 0.7


def test_load_agent_config_reads_memory_fields(tmp_path) -> None:
    payload = _base_agent_payload()
    payload["memory_window_messages"] = 15
    payload["include_topic_every_turn"] = False
    payload["temperature"] = 1.2

    config_path = tmp_path / "agents.json"
    config_path.write_text(json.dumps([payload]), encoding="utf-8")

    configs = load_agent_configs(config_path)

    assert len(configs) == 1
    assert configs[0].memory_window_messages == 15
    assert configs[0].include_topic_every_turn is False
    assert configs[0].temperature == 1.2


def test_load_agent_config_rejects_invalid_topic_flag(tmp_path) -> None:
    payload = _base_agent_payload()
    payload["include_topic_every_turn"] = {"bad": True}

    config_path = tmp_path / "agents.json"
    config_path.write_text(json.dumps([payload]), encoding="utf-8")

    with pytest.raises(ValueError, match="Invalid boolean value"):
        load_agent_configs(config_path)


def test_load_agent_config_rejects_invalid_temperature(tmp_path) -> None:
    payload = _base_agent_payload()
    payload["temperature"] = 2.5

    config_path = tmp_path / "agents.json"
    config_path.write_text(json.dumps([payload]), encoding="utf-8")

    with pytest.raises(ValueError, match="temperature must be between 0.0 and 2.0"):
        load_agent_configs(config_path)
