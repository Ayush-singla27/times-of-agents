from __future__ import annotations

import logging
import os
from contextlib import asynccontextmanager
from datetime import date
from typing import Any

import uvicorn
from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware

from times_of_agents.application.pipeline import DailyBriefingPipeline
from times_of_agents.application.scheduler import DailyJobScheduler
from times_of_agents.infrastructure.agent_config_file import load_agent_configs
from times_of_agents.infrastructure.backend_settings import BackendSettings
from times_of_agents.infrastructure.sqlite_news_store import SQLiteNewsStore

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logging.basicConfig(level=logging.INFO)


def _serialise_insight_chain(raw: dict[str, Any]) -> dict[str, Any]:
    topic_id = str(raw.get("topic_id", ""))
    return {
        "id": topic_id,
        "label": str(raw.get("label", "")),
        "title": str(raw.get("title", "")),
        "agentId": str(raw.get("agent_id", "")),
        "nodes": raw.get("nodes", []),
        "articleId": topic_id,
        "createdAt": str(raw.get("created_at", "")),
    }


def _serialise_agent(cfg: Any) -> dict[str, Any]:
    return {
        "id": cfg.identity.id,
        "name": cfg.identity.name,
        "role": cfg.identity.role,
        "description": cfg.identity.description,
        "emotion_profile": cfg.emotion_profile.to_dict(),
    }


def _validate_run_date(run_date: str) -> date:
    try:
        return date.fromisoformat(run_date)
    except ValueError as error:
        raise HTTPException(status_code=400, detail="run_date must be YYYY-MM-DD") from error


def _store_from_request(request: Request) -> SQLiteNewsStore:
    return request.app.state.store


def _pipeline_from_request(request: Request) -> DailyBriefingPipeline:
    return request.app.state.pipeline


def create_app(settings: BackendSettings | None = None) -> FastAPI:
    resolved_settings = settings or BackendSettings.from_config_file()

    @asynccontextmanager
    async def _lifespan(app: FastAPI):
        store = SQLiteNewsStore(resolved_settings.db_path)
        pipeline = DailyBriefingPipeline(
            store=store,
            agent_config_file=resolved_settings.agents_config_file,
            articles_dir=resolved_settings.articles_dir,
            model=resolved_settings.model,
            article_count=resolved_settings.article_count,
            rounds=resolved_settings.rounds,
            seed=resolved_settings.seed,
            write_articles_to_files=resolved_settings.write_articles_to_files,
            discussions_per_run=resolved_settings.discussions_per_run,
            insights_per_run=resolved_settings.insights_per_run,
        )
        scheduler = DailyJobScheduler(
            pipeline=pipeline,
            hour_utc=resolved_settings.schedule_hour_utc,
        )

        agent_configs = []
        if resolved_settings.agents_config_file.exists():
            try:
                agent_configs = load_agent_configs(resolved_settings.agents_config_file)
            except Exception:
                logger.exception("Failed to load agent configs")

        app.state.store = store
        app.state.pipeline = pipeline
        app.state.scheduler = scheduler
        app.state.agent_configs = agent_configs

        if resolved_settings.run_on_startup:
            try:
                pipeline.run_for_date()
            except Exception:
                logger.exception("Startup daily pipeline execution failed")
        if resolved_settings.enable_scheduler:
            scheduler.start()

        logger.info(
            "Times of Agents API ready on http://%s:%s",
            resolved_settings.host,
            resolved_settings.port,
        )

        try:
            yield
        finally:
            scheduler.stop()

    app = FastAPI(
        title="Times of Agents API",
        version="1.0.0",
        lifespan=_lifespan,
    )
    app.state.settings = resolved_settings

    cors_origins_raw = os.getenv("CORS_ALLOWED_ORIGINS", "")
    cors_origins = [o.strip() for o in cors_origins_raw.split(",") if o.strip()] or ["*"]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_origins,
        allow_credentials=cors_origins != ["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    # ── Agents ────────────────────────────────────────────────────────────────

    @app.get("/api/v1/agents")
    def list_agents(request: Request) -> list[dict[str, Any]]:
        return [_serialise_agent(cfg) for cfg in request.app.state.agent_configs]

    @app.get("/api/v1/agents/{agent_id}")
    def get_agent(agent_id: str, request: Request) -> dict[str, Any]:
        for cfg in request.app.state.agent_configs:
            if cfg.identity.id == agent_id:
                return _serialise_agent(cfg)
        raise HTTPException(status_code=404, detail=f"Agent not found: {agent_id}")

    # ── Articles (topics) ─────────────────────────────────────────────────────

    @app.get("/api/v1/articles")
    def list_articles(request: Request) -> list[dict[str, Any]]:
        store = _store_from_request(request)
        return store.get_all_topics(limit=20)

    @app.get("/api/v1/articles/{article_id}")
    def get_article(article_id: str, request: Request) -> dict[str, Any]:
        store = _store_from_request(request)
        article = store.get_topic(article_id)
        if article is None:
            raise HTTPException(status_code=404, detail=f"Article not found: {article_id}")
        return article

    @app.get("/api/v1/articles/{article_id}/debate")
    def get_article_debate(article_id: str, request: Request) -> dict[str, Any]:
        store = _store_from_request(request)
        discussion = store.get_discussion(article_id)
        if discussion is None:
            raise HTTPException(status_code=404, detail=f"Debate not found for article {article_id}")
        return discussion

    # ── Insight chains ────────────────────────────────────────────────────────

    @app.get("/api/v1/chains")
    def list_chains(
        request: Request,
        articleId: str | None = Query(default=None),
    ) -> list[dict[str, Any]]:
        store = _store_from_request(request)
        chains = store.get_all_insight_chains(article_id=articleId)
        return [_serialise_insight_chain(c) for c in chains]

    @app.get("/api/v1/articles/{article_id}/insight")
    def get_article_insight(article_id: str, request: Request) -> dict[str, Any]:
        store = _store_from_request(request)
        insight_chain = store.get_insight_chain(article_id)
        if insight_chain is None:
            raise HTTPException(status_code=404, detail=f"Insight chain not found for article {article_id}")
        return insight_chain

    @app.get("/api/v1/articles/{article_id}/deep_insight")
    def get_article_deep_insight(article_id: str, request: Request) -> dict[str, Any]:
        store = _store_from_request(request)
        deep_insight = store.get_deep_insight(article_id)
        if deep_insight is None:
            raise HTTPException(status_code=404, detail=f"Deep insight not found for article {article_id}")
        return deep_insight

    # ── Snapshots (run-level metadata) ────────────────────────────────────────

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

    # ── Admin ─────────────────────────────────────────────────────────────────

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
    settings = BackendSettings.from_config_file()
    uvicorn.run(
        "times_of_agents.interfaces.api.main:app",
        host=settings.host,
        port=settings.port,
        reload=False,
    )


if __name__ == "__main__":
    run()
