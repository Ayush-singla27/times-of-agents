from __future__ import annotations

import threading
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any

from times_of_agents.application.discussion_orchestrator import run_discussion
from times_of_agents.application.news_topic_agent import generate_topics_from_trending_news
from times_of_agents.infrastructure.agent_config_file import load_agent_configs
from times_of_agents.infrastructure.sqlite_news_store import SQLiteNewsStore


class DailyBriefingPipeline:
    """Runs the full daily flow: topic discovery plus selected topic discussions."""

    def __init__(
        self,
        *,
        store: SQLiteNewsStore,
        agent_config_file: Path,
        articles_dir: Path,
        model: str,
        article_count: int,
        rounds: int,
        seed: int,
        write_articles_to_files: bool = False,
        discussions_per_run: int = 1,
    ) -> None:
        self._store = store
        self._agent_config_file = agent_config_file
        self._articles_dir = articles_dir
        self._model = model
        self._article_count = article_count
        self._rounds = rounds
        self._seed = seed
        self._write_articles_to_files = write_articles_to_files
        self._discussions_per_run = discussions_per_run
        self._lock = threading.Lock()

    def run_for_date(self, *, target_date: date | None = None, force: bool = False) -> dict[str, Any]:
        run_date = (target_date or datetime.now(UTC).date()).isoformat()

        with self._lock:
            if self._store.has_run(run_date) and not force:
                snapshot = self._store.get_snapshot(run_date)
                if snapshot is None:
                    raise RuntimeError(f"Stored run is missing for date {run_date}")
                return snapshot

            topics = generate_topics_from_trending_news(
                model=self._model,
                article_count=self._article_count,
                write_articles_to_files=self._write_articles_to_files,
                articles_dir=self._articles_dir,
            )
            if not topics:
                raise RuntimeError("No topics were generated from daily news job")

            self._store.upsert_daily_run(
                run_date=run_date,
                model=self._model,
                article_count=len(topics),
                rounds=self._rounds,
                seed=self._seed,
            )
            self._store.replace_topics(run_date=run_date, topics=topics)

            agent_configs = load_agent_configs(self._agent_config_file)
            topics_to_discuss = topics[: self._discussions_per_run]
            for topic in topics_to_discuss:
                discussion_result = run_discussion(
                    topic=topic["content"],
                    agent_configs=agent_configs,
                    rounds=self._rounds,
                    seed=self._seed,
                    model=self._model,
                    interjections_enabled=True,
                )
                self._store.upsert_discussion(
                    topic_id=topic["topic_id"],
                    discussion_payload=discussion_result.to_dict(),
                )

            snapshot = self._store.get_snapshot(run_date)
            if snapshot is None:
                raise RuntimeError(f"Failed to read back run for date {run_date}")
            return snapshot

