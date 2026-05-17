from __future__ import annotations

import logging
from importlib import import_module
from typing import Any

from times_of_agents.application.pipeline import DailyBriefingPipeline

logger = logging.getLogger(__name__)


class DailyJobScheduler:
    def __init__(self, *, pipeline: DailyBriefingPipeline, hour_utc: int) -> None:
        self._pipeline = pipeline
        self._hour_utc = hour_utc
        self._scheduler: Any | None = None
        self._started = False

    def start(self) -> None:
        if self._started:
            return
        background_module = import_module("apscheduler.schedulers.background")
        cron_module = import_module("apscheduler.triggers.cron")
        background_scheduler_cls = getattr(background_module, "BackgroundScheduler")
        cron_trigger_cls = getattr(cron_module, "CronTrigger")

        self._scheduler = background_scheduler_cls(timezone="UTC")
        self._scheduler.add_job(
            self._safe_run,
            trigger=cron_trigger_cls(hour=self._hour_utc, timezone="UTC"),
            id="times-of-agents-daily-job",
            replace_existing=True,
        )
        self._scheduler.start()
        self._started = True
        logger.info("Started daily scheduler (hour_utc=%s)", self._hour_utc)

    def stop(self) -> None:
        if not self._started or self._scheduler is None:
            return
        self._scheduler.shutdown(wait=False)
        self._started = False
        self._scheduler = None
        logger.info("Stopped daily scheduler")

    def _safe_run(self) -> None:
        try:
            self._pipeline.run_for_date()
            logger.info("Daily pipeline run completed")
        except Exception:
            logger.exception("Daily pipeline run failed")
