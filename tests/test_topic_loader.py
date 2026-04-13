from pathlib import Path

import pytest

from agentpress_backend.infrastructure.topic_file import load_topic


def test_load_topic_success(tmp_path: Path) -> None:
    topic_file = tmp_path / "topic.txt"
    topic_file.write_text("Example topic", encoding="utf-8")

    assert load_topic(topic_file) == "Example topic"


def test_load_topic_empty_raises(tmp_path: Path) -> None:
    topic_file = tmp_path / "topic.txt"
    topic_file.write_text("\n", encoding="utf-8")

    with pytest.raises(ValueError):
        load_topic(topic_file)
