from pathlib import Path

import pytest

from times_of_agents.infrastructure.topic_file import load_topic, save_topic


def test_load_topic_success(tmp_path: Path) -> None:
    topic_file = tmp_path / "topic.txt"
    topic_file.write_text("Example topic", encoding="utf-8")

    assert load_topic(topic_file) == "Example topic"


def test_load_topic_empty_raises(tmp_path: Path) -> None:
    topic_file = tmp_path / "topic.txt"
    topic_file.write_text("\n", encoding="utf-8")

    with pytest.raises(ValueError):
        load_topic(topic_file)


def test_save_topic_round_trip(tmp_path: Path) -> None:
    topic_file = tmp_path / "nested" / "topic.txt"

    save_topic(topic_file, "  Fresh curated topic  ")

    assert load_topic(topic_file) == "Fresh curated topic"


def test_save_topic_empty_raises(tmp_path: Path) -> None:
    topic_file = tmp_path / "topic.txt"

    with pytest.raises(ValueError):
        save_topic(topic_file, "   ")
