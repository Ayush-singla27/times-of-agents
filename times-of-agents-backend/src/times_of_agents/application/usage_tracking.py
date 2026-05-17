from __future__ import annotations

import logging
from typing import Any

from times_of_agents.domain.entities import TokenUsageSummary
from times_of_agents.infrastructure.backend_settings import get_backend_settings

logger = logging.getLogger(__name__)


def estimate_tokens(text: str) -> int:
    if not text:
        return 0
    return max(1, (len(text) + 3) // 4)


def extract_usage_dict(source: Any) -> dict[str, Any] | None:
    for attr in ("token_usage", "usage", "usage_metrics", "llm_usage"):
        usage = getattr(source, attr, None)
        if isinstance(usage, dict):
            return usage
        if usage is not None:
            return {
                key: getattr(usage, key, None)
                for key in (
                    "prompt_tokens",
                    "completion_tokens",
                    "input_tokens",
                    "output_tokens",
                    "total_tokens",
                )
                if getattr(usage, key, None) is not None
            }
    return None


def normalize_usage(usage: dict[str, Any]) -> tuple[int, int, int]:
    input_tokens = int(usage.get("prompt_tokens") or usage.get("input_tokens") or usage.get("input") or 0)
    output_tokens = int(
        usage.get("completion_tokens") or usage.get("output_tokens") or usage.get("output") or 0
    )
    total_tokens = int(usage.get("total_tokens") or usage.get("total") or 0)
    if total_tokens == 0:
        total_tokens = input_tokens + output_tokens
    return input_tokens, output_tokens, total_tokens


def collect_usage_from_result(crew_result: Any) -> TokenUsageSummary:
    summary = TokenUsageSummary()
    sources = [crew_result] + list(getattr(crew_result, "tasks_output", []) or [])
    for source in sources:
        usage = extract_usage_dict(source)
        if not usage:
            continue
        input_tokens, output_tokens, total_tokens = normalize_usage(usage)
        if input_tokens == 0 and output_tokens == 0 and total_tokens == 0:
            continue
        summary.call_count += 1
        summary.input_tokens += input_tokens
        summary.output_tokens += output_tokens
        summary.total_tokens += total_tokens
    return summary


def merge_usage(target: TokenUsageSummary, addition: TokenUsageSummary) -> None:
    target.call_count += addition.call_count
    target.input_tokens += addition.input_tokens
    target.output_tokens += addition.output_tokens
    target.total_tokens += addition.total_tokens


def resolve_cost_rates() -> tuple[float, float]:
    settings = get_backend_settings()
    return settings.token_input_cost_per_1k_usd, settings.token_output_cost_per_1k_usd


def apply_costs(summary: TokenUsageSummary, input_rate: float, output_rate: float) -> None:
    summary.input_cost_usd = (summary.input_tokens / 1000.0) * input_rate
    summary.output_cost_usd = (summary.output_tokens / 1000.0) * output_rate
    summary.total_cost_usd = summary.input_cost_usd + summary.output_cost_usd


def log_agent_usage(
    agent_name: str,
    task_label: str,
    summary: TokenUsageSummary,
    input_rate: float,
    output_rate: float,
    *,
    estimated: bool = False,
) -> None:
    """Log one line of token + cost info for a single agent task."""
    est = " ~est" if estimated else ""
    tokens = (
        f"in={summary.input_tokens:,} out={summary.output_tokens:,} total={summary.total_tokens:,}"
    )
    if input_rate > 0.0 or output_rate > 0.0:
        cost = (summary.input_tokens / 1000.0) * input_rate + (summary.output_tokens / 1000.0) * output_rate
        logger.info("[%s] %s%s | %s | $%.6f", agent_name, task_label, est, tokens, cost)
    else:
        logger.info("[%s] %s%s | %s", agent_name, task_label, est, tokens)
