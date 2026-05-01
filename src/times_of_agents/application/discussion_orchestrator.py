from __future__ import annotations

from datetime import UTC, datetime
from random import Random
from typing import Any

from crewai import Crew, Process

from times_of_agents.application.agent_runtime import build_system_prompt
from times_of_agents.application.crew_agents import build_crewai_agent
from times_of_agents.application.crew_tasks import (
    build_interjection_task,
    build_interjection_task_prompt,
    build_speaking_task,
    build_speaking_task_prompt,
)
from times_of_agents.application.usage_tracking import (
    apply_costs,
    collect_usage_from_result,
    estimate_tokens,
    merge_usage,
    resolve_cost_rates,
)
from times_of_agents.domain.entities import AgentConfig, DiscussionResult, Message, TokenUsageSummary
from times_of_agents.infrastructure.llm_factory import create_crewai_llm


def _prepare_topic_for_prompt(topic: str) -> str:
    text = topic.strip()
    if "---" in text:
        text = text.split("---", 1)[1].strip()

    cleaned_lines: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith(("Topic ID:", "Source:", "Link:")):
            continue
        cleaned_lines.append(stripped)

    return "\n".join(cleaned_lines) if cleaned_lines else topic.strip()


def _order_configs_for_round(agent_configs: list[AgentConfig], rng: Random) -> list[AgentConfig]:
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
        respect_context_window=True,
    )
    return crew.kickoff()


def _estimate_usage_for_prompt(
    config: AgentConfig,
    description: str,
    expected_output: str,
    raw_content: str,
) -> TokenUsageSummary:
    prompt_text = build_system_prompt(config) + "\n\n" + description + "\n\n" + expected_output
    summary = TokenUsageSummary(call_count=1)
    summary.input_tokens = estimate_tokens(prompt_text)
    summary.output_tokens = estimate_tokens(raw_content)
    summary.total_tokens = summary.input_tokens + summary.output_tokens
    return summary


def _is_no_interjection(text: str) -> bool:
    return text.strip().upper() == "NO_INTERJECTION"


def _recent_messages(transcript: list[Message], memory_window_messages: int) -> list[Message]:
    if memory_window_messages <= 0:
        return []
    return transcript[-memory_window_messages:]


def _should_include_topic(
    config: AgentConfig,
    topic_shown_once: set[str],
) -> bool:
    if config.include_topic_every_turn:
        return True
    if config.identity.id in topic_shown_once:
        return False
    topic_shown_once.add(config.identity.id)
    return True


def run_discussion(
    topic: str,
    agent_configs: list[AgentConfig],
    rounds: int,
    seed: int = 42,
    model: str = "gpt-4o-mini",
    interjections_enabled: bool = True,
) -> DiscussionResult:
    if rounds <= 0:
        raise ValueError("rounds must be positive")
    if not agent_configs:
        raise ValueError("agent_configs must not be empty")

    rng = Random(seed)
    agents_by_id = {
        cfg.identity.id: build_crewai_agent(
            config=cfg,
            llm=create_crewai_llm(model=model, temperature=cfg.temperature),
        )
        for cfg in agent_configs
    }

    transcript: list[Message] = []
    usage_summary = TokenUsageSummary()
    used_estimate = False
    input_rate, output_rate = resolve_cost_rates()

    prompt_topic = _prepare_topic_for_prompt(topic)
    topic_shown_once: set[str] = set()

    for round_index in range(1, rounds + 1):
        ordered_configs = _order_configs_for_round(agent_configs, rng)
        interjected_ids: set[str] = set()

        for position, cfg in enumerate(ordered_configs):
            speaking_prior_messages = _recent_messages(transcript, cfg.memory_window_messages)
            speaking_include_topic = _should_include_topic(cfg, topic_shown_once)
            speaking_task = build_speaking_task(
                agent=agents_by_id[cfg.identity.id],
                topic=prompt_topic,
                round_index=round_index,
                prior_messages=speaking_prior_messages,
                include_topic=speaking_include_topic,
            )
            speaking_result = _run_single_task(agents_by_id[cfg.identity.id], speaking_task)
            raw_content = _task_raw_output(speaking_result, 0) or str(speaking_result).strip()

            speaking_usage = collect_usage_from_result(speaking_result)
            if speaking_usage.call_count == 0:
                description, expected_output = build_speaking_task_prompt(
                    topic=prompt_topic,
                    round_index=round_index,
                    prior_messages=speaking_prior_messages,
                    include_topic=speaking_include_topic,
                )
                speaking_usage = _estimate_usage_for_prompt(cfg, description, expected_output, raw_content)
                used_estimate = True
            merge_usage(usage_summary, speaking_usage)

            latest_message = Message(
                round_index=round_index,
                agent_id=cfg.identity.id,
                agent_name=cfg.identity.name,
                content=raw_content,
                dominant_emotion=cfg.emotion_profile.dominant_emotion(),
                is_interjection=False,
                created_at=datetime.now(UTC),
            )
            transcript.append(latest_message)

            if not interjections_enabled or position >= len(ordered_configs) - 1:
                continue

            for idx in range(position + 1, len(ordered_configs)):
                other_cfg = ordered_configs[idx]
                if other_cfg.identity.id in interjected_ids:
                    continue
                other_agent = agents_by_id[other_cfg.identity.id]
                interjection_prior_messages = _recent_messages(transcript, other_cfg.memory_window_messages)
                interjection_include_topic = _should_include_topic(other_cfg, topic_shown_once)
                interjection_task = build_interjection_task(
                    agent=other_agent,
                    topic=prompt_topic,
                    round_index=round_index,
                    prior_messages=interjection_prior_messages,
                    latest_message=latest_message,
                    include_topic=interjection_include_topic,
                )
                interjection_result = _run_single_task(other_agent, interjection_task)
                interjection_text = _task_raw_output(interjection_result, 0) or str(interjection_result).strip()

                interjection_usage = collect_usage_from_result(interjection_result)
                if interjection_usage.call_count == 0:
                    description, expected_output = build_interjection_task_prompt(
                        topic=prompt_topic,
                        round_index=round_index,
                        prior_messages=interjection_prior_messages,
                        latest_message=latest_message,
                        include_topic=interjection_include_topic,
                    )
                    interjection_usage = _estimate_usage_for_prompt(
                        other_cfg,
                        description,
                        expected_output,
                        interjection_text,
                    )
                    used_estimate = True
                merge_usage(usage_summary, interjection_usage)

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
                        is_interjection=True,
                        created_at=datetime.now(UTC),
                    )
                )

    apply_costs(usage_summary, input_rate, output_rate)
    _print_usage_summary(usage_summary, input_rate, output_rate, used_estimate)

    return DiscussionResult(
        topic=topic,
        rounds=rounds,
        transcript=transcript,
        usage_summary=usage_summary,
    )
