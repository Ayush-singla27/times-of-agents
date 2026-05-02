from __future__ import annotations

from times_of_agents.application.pipelines.daily_briefing_pipeline import DailyBriefingPipeline

# Backward-compatible alias for existing imports.
DailyNewsPipeline = DailyBriefingPipeline

__all__ = ["DailyBriefingPipeline", "DailyNewsPipeline"]
