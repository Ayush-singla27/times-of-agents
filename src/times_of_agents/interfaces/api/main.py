from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from datetime import date
from typing import Any

import uvicorn
from fastapi import FastAPI, HTTPException, Query, Request

from times_of_agents.application.pipelines.daily_briefing_pipeline import DailyBriefingPipeline
from times_of_agents.application.scheduling.daily_job_scheduler import DailyJobScheduler
from times_of_agents.infrastructure.backend_settings import BackendSettings
from times_of_agents.infrastructure.sqlite_news_store import SQLiteNewsStore

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logging.basicConfig(level=logging.INFO)


def _validate_run_date(run_date: str) -> date:
    try:
        return date.fromisoformat(run_date)
    except ValueError as error:
        raise HTTPException(status_code=400, detail="run_date must be YYYY-MM-DD") from error


def _store_from_request(request: Request) -> SQLiteNewsStore:
    return request.app.state.store


def _pipeline_from_request(request: Request) -> DailyBriefingPipeline:
    return request.app.state.pipeline


@asynccontextmanager
async def _lifespan(app: FastAPI):
    settings: BackendSettings = app.state.settings
    store = SQLiteNewsStore(settings.db_path)
    pipeline = DailyBriefingPipeline(
        store=store,
        agent_config_file=settings.agents_config_file,
        articles_dir=settings.articles_dir,
        model=settings.model,
        article_count=settings.article_count,
        rounds=settings.rounds,
        seed=settings.seed,
        write_articles_to_files=settings.write_articles_to_files,
        discussions_per_run=settings.discussions_per_run,
    )

    scheduler = DailyJobScheduler(
        pipeline=pipeline,
        hour_utc=settings.schedule_hour_utc,
    )

    app.state.store = store
    app.state.pipeline = pipeline
    app.state.scheduler = scheduler
    if settings.run_on_startup:
        try:
            pipeline.run_for_date()
        except Exception:
            logger.exception("Startup daily pipeline execution failed")
    if settings.enable_scheduler:
        scheduler.start()

    try:
        yield
    finally:
        scheduler.stop()


def create_app(settings: BackendSettings | None = None) -> FastAPI:
    app = FastAPI(
        title="Times of Agents API",
        version="1.0.0",
    )
    app.state.settings = settings or BackendSettings.from_config_file()
    app.router.lifespan_context = _lifespan

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/api/v1/snapshots/latest")
    def get_latest_snapshot(request: Request) -> dict[str, Any]:
        store = _store_from_request(request)
        run_date = store.get_latest_run_date()
        if run_date is None:
            raise HTTPException(status_code=404, detail="No snapshots available")

        snapshot = store.get_snapshot(run_date)
        if snapshot is None:
            raise HTTPException(status_code=404, detail="No snapshots available")
        return snapshot

    @app.get("/api/v1/snapshots/{run_date}")
    def get_snapshot(run_date: str, request: Request) -> dict[str, Any]:
        _validate_run_date(run_date)

        store = _store_from_request(request)
        snapshot = store.get_snapshot(run_date)
        if snapshot is None:
            raise HTTPException(status_code=404, detail=f"Snapshot not found for date {run_date}")
        return snapshot

    @app.get("/api/v1/topics/{topic_id}")
    def get_topic(topic_id: str, request: Request) -> dict[str, Any]:
        store = _store_from_request(request)
        topic = store.get_topic(topic_id)
        if topic is None:
            raise HTTPException(status_code=404, detail=f"Topic not found: {topic_id}")
        return topic

    @app.get("/api/v1/topics/{topic_id}/discussion")
    def get_topic_discussion(topic_id: str, request: Request) -> dict[str, Any]:
        store = _store_from_request(request)
        discussion = store.get_discussion(topic_id)
        if discussion is None:
            raise HTTPException(status_code=404, detail=f"Discussion not found for topic {topic_id}")
        return discussion

    @app.post("/api/v1/admin/run-daily-job")
    def run_daily_job(
        request: Request,
        force: bool = Query(default=False),
        run_date: str | None = Query(default=None, description="Optional YYYY-MM-DD override"),
    ) -> dict[str, Any]:
        pipeline = _pipeline_from_request(request)

        target_date = None
        if run_date is not None:
            target_date = _validate_run_date(run_date)

        return pipeline.run_for_date(target_date=target_date, force=force)

    return app


app = create_app()


def run() -> None:
    uvicorn.run("times_of_agents.interfaces.api.main:app", host="0.0.0.0", port=8000, reload=False)


if __name__ == "__main__":
    run()
