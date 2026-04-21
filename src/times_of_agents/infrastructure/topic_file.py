from __future__ import annotations

from pathlib import Path


def load_topic(topic_file: Path) -> str:
    if not topic_file.exists():
        raise FileNotFoundError(f"Topic file not found: {topic_file}")

    topic = topic_file.read_text(encoding="utf-8").strip()
    if not topic:
        raise ValueError("Topic file is empty")

    return topic


def save_topic(topic_file: Path, topic: str) -> None:
    cleaned = topic.strip()
    if not cleaned:
        raise ValueError("Generated topic is empty")

    topic_file.parent.mkdir(parents=True, exist_ok=True)
    topic_file.write_text(cleaned + "\n", encoding="utf-8")
