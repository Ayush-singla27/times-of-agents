from __future__ import annotations

import json
import logging
import re
from datetime import UTC, datetime
from typing import Any

from crewai import Agent, Crew, LLM, Process, Task

from times_of_agents.application.agent_builder import make_step_callback
from times_of_agents.application.usage_tracking import collect_usage_from_result, log_agent_usage, resolve_cost_rates
from times_of_agents.domain.entities import TokenUsageSummary
from times_of_agents.infrastructure.tavily_search import tavily_search_tool

logger = logging.getLogger(__name__)

_AGENT_ID = "insight-analyst"
_AGENT_DISPLAY = "Insight Analyst"


def _build_insight_agent(model: str) -> Agent:
    llm = LLM(model=model)
    return Agent(
        role="Senior Investigative Analyst",
        goal=(
            "Research news topics deeply using web search and produce structured, "
            "professional analysis that reveals cause-effect chains and expert conclusions."
        ),
        backstory=(
            "You are a senior analyst with expertise in geopolitics, economics, and technology. "
            "You use evidence-based reasoning, cite sources from your research, and present "
            "findings in clear, structured formats. You always search the web for current "
            "information before forming conclusions."
        ),
        tools=[tavily_search_tool],
        llm=llm,
        verbose=False,
        allow_delegation=False,
        memory=False,
        step_callback=make_step_callback(_AGENT_DISPLAY),
    )


def _extract_json(text: str) -> dict[str, Any]:
    """Extract the first JSON object from LLM text output."""
    text = text.strip()

    # Try direct parse first
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Try markdown code block
    block_match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if block_match:
        try:
            return json.loads(block_match.group(1))
        except json.JSONDecodeError:
            pass

    # Try finding the first {...} span
    brace_match = re.search(r"\{.*\}", text, re.DOTALL)
    if brace_match:
        try:
            return json.loads(brace_match.group(0))
        except json.JSONDecodeError:
            pass

    raise ValueError(f"Could not extract JSON from LLM output: {text[:200]}")


def _trim_to_words(text: str, max_words: int) -> str:
    words = text.split()
    if len(words) <= max_words:
        return text
    return " ".join(words[:max_words]).rstrip(",.;:") + "…"


def _fallback_insight_chain(topic_id: str) -> dict[str, Any]:
    return {
        "topic_id": topic_id,
        "agent_id": _AGENT_ID,
        "label": "Analysis Pending",
        "title": "Insight chain could not be generated at this time.",
        "nodes": [],
        "created_at": datetime.now(UTC).isoformat(),
    }


def _fallback_deep_insight(topic_id: str) -> dict[str, Any]:
    return {
        "topic_id": topic_id,
        "agent_id": _AGENT_ID,
        "conclusion": "Deep insight could not be generated at this time.",
        "key_findings": [],
        "confidence_level": "Low",
        "confidence_reason": "Generation failed.",
        "created_at": datetime.now(UTC).isoformat(),
    }


def generate_insight_chain(topic_id: str, topic_content: str, model: str) -> tuple[dict[str, Any], TokenUsageSummary]:
    """
    Generate a causal insight chain for a news topic.
    Returns (result_dict, usage) where result_dict has label, title, nodes[], topic_id, agent_id, created_at.
    """
    try:
        agent = _build_insight_agent(model)
        task = Task(
            description=(
                f"Research this news topic using web search:\n\n{topic_content}\n\n"
                "Then produce a causal insight chain showing how this event unfolds. "
                "Search for at least 2 related queries to gather context.\n\n"
                "Return ONLY a JSON object with this exact structure (no other text):\n"
                "{\n"
                '  "label": "<short 2-3 word label for the chain>",\n'
                '  "title": "<one sentence thesis about the causal chain>",\n'
                '  "nodes": [\n'
                '    {"step": "Trigger", "icon": "<emoji>", "title": "<short title>", "description": "<1-2 sentence explanation>"},\n'
                '    {"step": "Step 2", "icon": "<emoji>", "title": "<short title>", "description": "<1-2 sentence explanation>"},\n'
                '    {"step": "Step 3", "icon": "<emoji>", "title": "<short title>", "description": "<1-2 sentence explanation>"},\n'
                '    {"step": "Outcome", "icon": "<emoji>", "title": "<short title>", "description": "<1-2 sentence explanation>"}\n'
                "  ]\n"
                "}"
            ),
            expected_output="A JSON object representing the insight chain with label, title, and nodes array.",
            agent=agent,
        )
        crew = Crew(agents=[agent], tasks=[task], process=Process.sequential, verbose=False)
        result = crew.kickoff()
        input_rate, output_rate = resolve_cost_rates()
        usage = collect_usage_from_result(result)
        log_agent_usage(_AGENT_DISPLAY, f"insight_chain {topic_id}", usage, input_rate, output_rate)
        raw_text = str(result.raw) if hasattr(result, "raw") else str(result)
        parsed = _extract_json(raw_text)

        return {
            "topic_id": topic_id,
            "agent_id": _AGENT_ID,
            "label": str(parsed.get("label", "")),
            "title": str(parsed.get("title", "")),
            "nodes": parsed.get("nodes", []),
            "created_at": datetime.now(UTC).isoformat(),
        }, usage
    except Exception:
        logger.exception("Failed to generate insight chain for topic %s", topic_id)
        return _fallback_insight_chain(topic_id), TokenUsageSummary()


def generate_deep_insight(topic_id: str, topic_content: str, model: str) -> tuple[dict[str, Any], TokenUsageSummary]:
    """
    Generate a deep professional analysis for a news topic.
    Returns (result_dict, usage) where result_dict has conclusion, key_findings[], confidence_level,
    confidence_reason, topic_id, agent_id, created_at.
    """
    try:
        agent = _build_insight_agent(model)
        task = Task(
            description=(
                f"Research this news topic thoroughly using web search:\n\n{topic_content}\n\n"
                "Search for multiple angles: background context, expert opinions, historical precedents, "
                "and potential future implications. Conduct at least 3 searches.\n\n"
                "Then write a deep professional analysis. "
                "Return ONLY a JSON object with this exact structure (no other text):\n"
                "{\n"
                '  "conclusion": "<3-5 sentence professional conclusion — STRICTLY under 250 words>",\n'
                '  "key_findings": [\n'
                '    "<finding 1: one concrete, evidence-backed insight — max 30 words>",\n'
                '    "<finding 2: one concrete, evidence-backed insight — max 30 words>",\n'
                '    "<finding 3: one concrete, evidence-backed insight — max 30 words>"\n'
                "  ],\n"
                '  "confidence_level": "High" | "Medium" | "Low",\n'
                '  "confidence_reason": "<one sentence explaining your confidence level>"\n'
                "}"
            ),
            expected_output="A JSON object with conclusion, key_findings array, confidence_level, and confidence_reason.",
            agent=agent,
        )
        crew = Crew(agents=[agent], tasks=[task], process=Process.sequential, verbose=False)
        result = crew.kickoff()
        input_rate, output_rate = resolve_cost_rates()
        usage = collect_usage_from_result(result)
        log_agent_usage(_AGENT_DISPLAY, f"deep_insight {topic_id}", usage, input_rate, output_rate)
        raw_text = str(result.raw) if hasattr(result, "raw") else str(result)
        parsed = _extract_json(raw_text)

        return {
            "topic_id": topic_id,
            "agent_id": _AGENT_ID,
            "conclusion": _trim_to_words(str(parsed.get("conclusion", "")), 300),
            "key_findings": [_trim_to_words(str(f), 40) for f in parsed.get("key_findings", [])],
            "confidence_level": str(parsed.get("confidence_level", "Medium")),
            "confidence_reason": str(parsed.get("confidence_reason", "")),
            "created_at": datetime.now(UTC).isoformat(),
        }, usage
    except Exception:
        logger.exception("Failed to generate deep insight for topic %s", topic_id)
        return _fallback_deep_insight(topic_id), TokenUsageSummary()
