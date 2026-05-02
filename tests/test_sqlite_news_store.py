from __future__ import annotations

from pathlib import Path

from times_of_agents.infrastructure.sqlite_news_store import SQLiteNewsStore


def test_sqlite_news_store_round_trip(tmp_path: Path) -> None:
    store = SQLiteNewsStore(tmp_path / "news.db")

    store.upsert_daily_run(
        run_date="2026-05-01",
        model="gpt-4o-mini",
        article_count=1,
        rounds=2,
        seed=42,
    )
    store.replace_topics(
        run_date="2026-05-01",
        topics=[
            {
                "topic_id": "topic-abc123",
                "title": "Test title",
                "source": "Test Source",
                "link": "https://example.com/news",
                "description": "Short description",
                "search_summary": "Longer summary",
                "content": "Raw topic content",
                "sort_order": 1,
            }
        ],
    )
    store.upsert_discussion(
        topic_id="topic-abc123",
        discussion_payload={"topic": "Test title", "rounds": 2, "transcript": []},
    )

    latest = store.get_latest_run_date()
    assert latest == "2026-05-01"

    snapshot = store.get_snapshot("2026-05-01")
    assert snapshot is not None
    assert snapshot["run_date"] == "2026-05-01"
    assert len(snapshot["topics"]) == 1
    assert snapshot["topics"][0]["topic_id"] == "topic-abc123"
    assert snapshot["topics"][0]["has_discussion"] is True

    topic = store.get_topic("topic-abc123")
    assert topic is not None
    assert topic["title"] == "Test title"

    discussion = store.get_discussion("topic-abc123")
    assert discussion is not None
    assert discussion["rounds"] == 2

