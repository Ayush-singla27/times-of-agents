from __future__ import annotations

from pathlib import Path


def load_topic(topic_file: Path) -> str:
    if not topic_file.exists():
        raise FileNotFoundError(f"Topic file not found: {topic_file}")

    topic = topic_file.read_text(encoding="utf-8").strip()
    if not topic:
        raise ValueError("Topic file is empty")

    return topic
