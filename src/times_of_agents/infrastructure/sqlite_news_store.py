from __future__ import annotations

import json
import sqlite3
from contextlib import contextmanager
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterator


class SQLiteNewsStore:
    def __init__(self, db_path: Path) -> None:
        self._db_path = db_path
        self._db_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize_schema()

    @contextmanager
    def _connection(self) -> Iterator[sqlite3.Connection]:
        conn = sqlite3.connect(self._db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()

    def _initialize_schema(self) -> None:
        with self._connection() as conn:
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS daily_runs (
                    run_date TEXT PRIMARY KEY,
                    created_at TEXT NOT NULL,
                    model TEXT NOT NULL,
                    article_count INTEGER NOT NULL,
                    rounds INTEGER NOT NULL,
                    seed INTEGER NOT NULL
                );

                CREATE TABLE IF NOT EXISTS topics (
                    topic_id TEXT PRIMARY KEY,
                    run_date TEXT NOT NULL,
                    title TEXT NOT NULL,
                    source TEXT NOT NULL,
                    link TEXT NOT NULL,
                    description TEXT NOT NULL,
                    search_summary TEXT NOT NULL,
                    content TEXT NOT NULL,
                    sort_order INTEGER NOT NULL,
                    FOREIGN KEY(run_date) REFERENCES daily_runs(run_date) ON DELETE CASCADE
                );

                CREATE TABLE IF NOT EXISTS discussions (
                    topic_id TEXT PRIMARY KEY,
                    discussion_json TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY(topic_id) REFERENCES topics(topic_id) ON DELETE CASCADE
                );

                CREATE INDEX IF NOT EXISTS idx_topics_run_date ON topics(run_date);
                """
            )

    def upsert_daily_run(
        self,
        *,
        run_date: str,
        model: str,
        article_count: int,
        rounds: int,
        seed: int,
    ) -> None:
        created_at = datetime.now(UTC).isoformat()
        with self._connection() as conn:
            conn.execute(
                """
                INSERT INTO daily_runs(run_date, created_at, model, article_count, rounds, seed)
                VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(run_date)
                DO UPDATE SET
                    created_at=excluded.created_at,
                    model=excluded.model,
                    article_count=excluded.article_count,
                    rounds=excluded.rounds,
                    seed=excluded.seed
                """,
                (run_date, created_at, model, article_count, rounds, seed),
            )

    def replace_topics(self, *, run_date: str, topics: list[dict[str, Any]]) -> None:
        with self._connection() as conn:
            conn.execute("DELETE FROM topics WHERE run_date = ?", (run_date,))
            for item in topics:
                conn.execute(
                    """
                    INSERT INTO topics(
                        topic_id, run_date, title, source, link,
                        description, search_summary, content, sort_order
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        item["topic_id"],
                        run_date,
                        item["title"],
                        item["source"],
                        item["link"],
                        item["description"],
                        item["search_summary"],
                        item["content"],
                        item["sort_order"],
                    ),
                )

    def upsert_discussion(self, *, topic_id: str, discussion_payload: dict[str, Any]) -> None:
        created_at = datetime.now(UTC).isoformat()
        with self._connection() as conn:
            conn.execute(
                """
                INSERT INTO discussions(topic_id, discussion_json, created_at)
                VALUES (?, ?, ?)
                ON CONFLICT(topic_id)
                DO UPDATE SET
                    discussion_json=excluded.discussion_json,
                    created_at=excluded.created_at
                """,
                (topic_id, json.dumps(discussion_payload), created_at),
            )

    def get_latest_run_date(self) -> str | None:
        with self._connection() as conn:
            row = conn.execute(
                "SELECT run_date FROM daily_runs ORDER BY run_date DESC LIMIT 1"
            ).fetchone()
        return None if row is None else str(row["run_date"])

    def has_run(self, run_date: str) -> bool:
        with self._connection() as conn:
            row = conn.execute(
                "SELECT 1 FROM daily_runs WHERE run_date = ? LIMIT 1",
                (run_date,),
            ).fetchone()
        return row is not None

    def get_snapshot(self, run_date: str) -> dict[str, Any] | None:
        with self._connection() as conn:
            run_row = conn.execute(
                "SELECT * FROM daily_runs WHERE run_date = ?",
                (run_date,),
            ).fetchone()
            if run_row is None:
                return None

            topic_rows = conn.execute(
                """
                SELECT
                    t.topic_id,
                    t.title,
                    t.source,
                    t.link,
                    t.description,
                    t.search_summary,
                    t.sort_order,
                    CASE WHEN d.topic_id IS NULL THEN 0 ELSE 1 END AS has_discussion
                FROM topics t
                LEFT JOIN discussions d ON d.topic_id = t.topic_id
                WHERE t.run_date = ?
                ORDER BY t.sort_order ASC
                """,
                (run_date,),
            ).fetchall()

        return {
            "run_date": str(run_row["run_date"]),
            "created_at": str(run_row["created_at"]),
            "model": str(run_row["model"]),
            "article_count": int(run_row["article_count"]),
            "rounds": int(run_row["rounds"]),
            "seed": int(run_row["seed"]),
            "topics": [
                {
                    "topic_id": str(row["topic_id"]),
                    "title": str(row["title"]),
                    "source": str(row["source"]),
                    "link": str(row["link"]),
                    "description": str(row["description"]),
                    "search_summary": str(row["search_summary"]),
                    "has_discussion": bool(row["has_discussion"]),
                }
                for row in topic_rows
            ],
        }

    def get_topic(self, topic_id: str) -> dict[str, Any] | None:
        with self._connection() as conn:
            row = conn.execute(
                """
                SELECT topic_id, run_date, title, source, link, description, search_summary, content
                FROM topics
                WHERE topic_id = ?
                """,
                (topic_id,),
            ).fetchone()

        if row is None:
            return None

        return {
            "topic_id": str(row["topic_id"]),
            "run_date": str(row["run_date"]),
            "title": str(row["title"]),
            "source": str(row["source"]),
            "link": str(row["link"]),
            "description": str(row["description"]),
            "search_summary": str(row["search_summary"]),
            "content": str(row["content"]),
        }

    def get_discussion(self, topic_id: str) -> dict[str, Any] | None:
        with self._connection() as conn:
            row = conn.execute(
                """
                SELECT discussion_json
                FROM discussions
                WHERE topic_id = ?
                """,
                (topic_id,),
            ).fetchone()

        if row is None:
            return None
        return json.loads(str(row["discussion_json"]))

