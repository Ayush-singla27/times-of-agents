from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from times_of_agents.infrastructure.backend_settings import BackendSettings
from times_of_agents.infrastructure.sqlite_news_store import SQLiteNewsStore
from times_of_agents.interfaces.api.main import create_app


def _seed_snapshot(db_path: Path) -> None:
    store = SQLiteNewsStore(db_path)
    store.upsert_daily_run(
        run_date="2026-05-01",
        model="gpt-4o-mini",
        article_count=1,
        rounds=3,
        seed=42,
    )
    store.replace_topics(
        run_date="2026-05-01",
        topics=[
            {
                "topic_id": "topic-seeded",
                "title": "Seeded topic",
                "source": "Example Source",
                "link": "https://example.com/seeded",
                "description": "Seeded description",
                "search_summary": "Seeded summary",
                "content": "Seeded topic content",
                "sort_order": 1,
            }
        ],
    )
    store.upsert_discussion(
        topic_id="topic-seeded",
        discussion_payload={"topic": "Seeded topic", "rounds": 3, "transcript": []},
    )


def test_get_latest_snapshot_and_topic_routes(tmp_path: Path) -> None:
    db_path = tmp_path / "api.db"
    _seed_snapshot(db_path)

    settings = BackendSettings(
        db_path=db_path,
        agents_config_file=tmp_path / "agents.json",
        articles_dir=tmp_path / "articles",
        run_on_startup=False,
        enable_scheduler=False,
    )
    app = create_app(settings)

    with TestClient(app) as client:
        latest = client.get("/api/v1/snapshots/latest")
        assert latest.status_code == 200
        assert latest.json()["run_date"] == "2026-05-01"

        topic = client.get("/api/v1/topics/topic-seeded")
        assert topic.status_code == 200
        assert topic.json()["title"] == "Seeded topic"

        discussion = client.get("/api/v1/topics/topic-seeded/discussion")
        assert discussion.status_code == 200
        assert discussion.json()["rounds"] == 3


def test_admin_run_daily_job_endpoint_uses_pipeline(tmp_path: Path) -> None:
    settings = BackendSettings(
        db_path=tmp_path / "api.db",
        agents_config_file=tmp_path / "agents.json",
        articles_dir=tmp_path / "articles",
        run_on_startup=False,
        enable_scheduler=False,
    )
    app = create_app(settings)

    class FakePipeline:
        def run_for_date(self, *, target_date=None, force=False):
            return {
                "run_date": "2026-05-01" if target_date is None else target_date.isoformat(),
                "force": force,
                "topics": [],
            }

    with TestClient(app) as client:
        client.app.state.pipeline = FakePipeline()
        response = client.post("/api/v1/admin/run-daily-job?force=true&run_date=2026-05-01")

    assert response.status_code == 200
    payload = response.json()
    assert payload["run_date"] == "2026-05-01"
    assert payload["force"] is True

