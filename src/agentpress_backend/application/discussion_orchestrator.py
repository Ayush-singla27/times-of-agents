from __future__ import annotations

from datetime import UTC, datetime
from random import Random
from typing import Any

import os
from crewai import Crew, Process

from agentpress_backend.application.agent_runtime import build_system_prompt
from agentpress_backend.application.crew_agents import build_crewai_agent
from agentpress_backend.application.crew_tasks import (
    build_interjection_task,
    build_interjection_task_prompt,
    build_speaking_task,
    build_speaking_task_prompt,
)
from agentpress_backend.domain.entities import (
    AgentConfig,
    DiscussionResult,
    Message,
    TokenUsageSummary,
)
from agentpress_backend.infrastructure.llm_factory import create_crewai_llm


def _order_configs_for_round(
    agent_configs: list[AgentConfig], rng: Random
) -> list[AgentConfig]:
    return sorted(
        agent_configs,
        key=lambda cfg: rng.random() * cfg.speaking_weight,
        reverse=True,
    )


def _task_raw_output(crew_result: Any, task_index: int) -> str:
    task_outputs = getattr(crew_result, "tasks_output", [])
    if task_index < len(task_outputs):
        return (getattr(task_outputs[task_index], "raw", "") or "").strip()
    return ""


def _estimate_tokens(text: str) -> int:
    if not text:
        return 0
    return max(1, (len(text) + 3) // 4)


def _extract_usage_dict(source: Any) -> dict[str, Any] | None:
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


def _normalize_usage(usage: dict[str, Any]) -> tuple[int, int, int]:
    input_tokens = int(
        usage.get("prompt_tokens")
        or usage.get("input_tokens")
        or usage.get("input")
        or 0
    )
    output_tokens = int(
        usage.get("completion_tokens")
        or usage.get("output_tokens")
        or usage.get("output")
        or 0
    )
    total_tokens = int(usage.get("total_tokens") or usage.get("total") or 0)
    if total_tokens == 0:
        total_tokens = input_tokens + output_tokens
    return input_tokens, output_tokens, total_tokens


def _collect_usage_from_result(crew_result: Any) -> TokenUsageSummary:
    summary = TokenUsageSummary()
    sources = [crew_result] + list(getattr(crew_result, "tasks_output", []) or [])
    for source in sources:
        usage = _extract_usage_dict(source)
        if not usage:
            continue
        input_tokens, output_tokens, total_tokens = _normalize_usage(usage)
        if input_tokens == 0 and output_tokens == 0 and total_tokens == 0:
            continue
        summary.call_count += 1
        summary.input_tokens += input_tokens
        summary.output_tokens += output_tokens
        summary.total_tokens += total_tokens
    return summary


def _resolve_cost_rates() -> tuple[float, float]:
    input_rate = os.getenv("TOKEN_INPUT_COST_PER_1K_USD")
    output_rate = os.getenv("TOKEN_OUTPUT_COST_PER_1K_USD")
    return float(input_rate or 0.0), float(output_rate or 0.0)


def _apply_costs(summary: TokenUsageSummary, input_rate: float, output_rate: float) -> None:
    summary.input_cost_usd = (summary.input_tokens / 1000.0) * input_rate
    summary.output_cost_usd = (summary.output_tokens / 1000.0) * output_rate
    summary.total_cost_usd = summary.input_cost_usd + summary.output_cost_usd


def _print_usage_summary(
    summary: TokenUsageSummary,
    input_rate: float,
    output_rate: float,
    used_estimate: bool,
) -> None:
    estimate_note = " (estimated)" if used_estimate else ""
    print(
        "Token usage%s: input=%s, output=%s, total=%s, calls=%s"
        % (
            estimate_note,
            summary.input_tokens,
            summary.output_tokens,
            summary.total_tokens,
            summary.call_count,
        )
    )
    if input_rate == 0.0 and output_rate == 0.0:
        print(
            "Token cost: $0.000000 (set TOKEN_INPUT_COST_PER_1K_USD and "
            "TOKEN_OUTPUT_COST_PER_1K_USD to enable cost estimation)"
        )
    else:
        print(
            "Token cost: $%.6f (input $%.6f + output $%.6f, rates: $%.4f/$%.4f per 1K)"
            % (
                summary.total_cost_usd,
                summary.input_cost_usd,
                summary.output_cost_usd,
                input_rate,
                output_rate,
            )
        )


def _run_single_task(agent: Any, task: Any) -> Any:
    crew = Crew(
        agents=[agent],
        tasks=[task],
        process=Process.sequential,
        verbose=False,
        memory=False,
    )
    return crew.kickoff()


def _estimate_usage_for_prompt(
    config: AgentConfig, description: str, expected_output: str, raw_content: str
) -> TokenUsageSummary:
    prompt_text = build_system_prompt(config) + "\n\n" + description + "\n\n" + expected_output
    summary = TokenUsageSummary(call_count=1)
    summary.input_tokens = _estimate_tokens(prompt_text)
    summary.output_tokens = _estimate_tokens(raw_content)
    summary.total_tokens = summary.input_tokens + summary.output_tokens
    return summary


def _merge_usage(target: TokenUsageSummary, addition: TokenUsageSummary) -> None:
    target.call_count += addition.call_count
    target.input_tokens += addition.input_tokens
    target.output_tokens += addition.output_tokens
    target.total_tokens += addition.total_tokens


def _is_no_interjection(text: str) -> bool:
    return text.strip().upper() == "NO_INTERJECTION"


class RoundDiscussionCrew:

    def __init__(
        self,
        *,
        agent_configs: list[AgentConfig],
        llm: Any,
        topic: str,
        round_index: int,
        transcript: list[Message],
    ) -> None:
        self.agent_configs = agent_configs
        self.llm = llm
        self.topic = topic
        self.round_index = round_index
        self.transcript = transcript
        self.agents = [build_crewai_agent(config=cfg, llm=self.llm) for cfg in self.agent_configs]
        self.tasks = [
            build_speaking_task(
                agent=self.agents[i],
                agent_name=cfg.identity.name,
                topic=self.topic,
                round_index=self.round_index,
                prior_messages=self.transcript[-8:],
            )
            for i, cfg in enumerate(self.agent_configs)
        ]

    def assemble(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=False,
            memory=False,
        )


def run_discussion(
    topic: str,
    agent_configs: list[AgentConfig],
    rounds: int,
    seed: int = 42,
    model: str = "claude-sonnet-4-5",
    interjections_enabled: bool = True,
) -> DiscussionResult:
    if rounds <= 0:
        raise ValueError("rounds must be positive")
    if not agent_configs:
        raise ValueError("agent_configs must not be empty")

    rng = Random(seed)
    llm = create_crewai_llm(model=model)

    transcript: list[Message] = []
    usage_summary = TokenUsageSummary()
    used_estimate = False
    input_rate, output_rate = _resolve_cost_rates()

    for round_index in range(1, rounds + 1):
        ordered_configs = _order_configs_for_round(agent_configs, rng)
        round_crew = RoundDiscussionCrew(
            agent_configs=ordered_configs,
            llm=llm,
            topic=topic,
            round_index=round_index,
            transcript=transcript,
        )
        ordered_agents = round_crew.agents
        interjected_ids: set[str] = set()

        crew_result = round_crew.assemble().kickoff()
        round_usage = _collect_usage_from_result(crew_result)
        if round_usage.call_count == 0:
            for cfg in ordered_configs:
                description, expected_output = build_speaking_task_prompt(
                    agent_name=cfg.identity.name,
                    topic=topic,
                    round_index=round_index,
                    prior_messages=transcript[-8:],
                )
                estimated = _estimate_usage_for_prompt(
                    cfg, description, expected_output, ""
                )
                _merge_usage(round_usage, estimated)
            used_estimate = True
        _merge_usage(usage_summary, round_usage)

        for position, (cfg, agent) in enumerate(zip(ordered_configs, ordered_agents, strict=True)):
            raw_content = _task_raw_output(crew_result, position)
            if not raw_content:
                raw_content = str(crew_result).strip()

            latest_message = Message(
                round_index=round_index,
                agent_id=cfg.identity.id,
                agent_name=cfg.identity.name,
                content=raw_content,
                dominant_emotion=cfg.emotion_profile.dominant_emotion(),
                created_at=datetime.now(UTC),
            )
            transcript.append(latest_message)

            if not interjections_enabled or position >= len(ordered_configs) - 1:
                continue

            for idx in range(position + 1, len(ordered_configs)):
                other_cfg = ordered_configs[idx]
                if other_cfg.identity.id in interjected_ids:
                    continue
                other_agent = ordered_agents[idx]
                interjection_task = build_interjection_task(
                    agent=other_agent,
                    agent_name=other_cfg.identity.name,
                    topic=topic,
                    round_index=round_index,
                    prior_messages=transcript[-8:],
                    latest_message=latest_message,
                )
                interjection_result = _run_single_task(other_agent, interjection_task)
                interjection_text = _task_raw_output(interjection_result, 0) or str(
                    interjection_result
                ).strip()

                interjection_usage = _collect_usage_from_result(interjection_result)
                if interjection_usage.call_count == 0:
                    description, expected_output = build_interjection_task_prompt(
                        agent_name=other_cfg.identity.name,
                        topic=topic,
                        round_index=round_index,
                        prior_messages=transcript[-8:],
                        latest_message=latest_message,
                    )
                    interjection_usage = _estimate_usage_for_prompt(
                        other_cfg,
                        description,
                        expected_output,
                        interjection_text,
                    )
                    used_estimate = True
                _merge_usage(usage_summary, interjection_usage)

                if not interjection_text or _is_no_interjection(interjection_text):
                    continue

                interjected_ids.add(other_cfg.identity.id)
                transcript.append(
                    Message(
                        round_index=round_index,
                        agent_id=other_cfg.identity.id,
                        agent_name=other_cfg.identity.name,
                        content=interjection_text,
                        dominant_emotion=other_cfg.emotion_profile.dominant_emotion(),
                        created_at=datetime.now(UTC),
                    )
                )

    _apply_costs(usage_summary, input_rate, output_rate)
    _print_usage_summary(usage_summary, input_rate, output_rate, used_estimate)

    return DiscussionResult(
        topic=topic,
        rounds=rounds,
        transcript=transcript,
        usage_summary=usage_summary,
    )
