from __future__ import annotations

import logging
from typing import Any

from crewai import Agent, LLM

from times_of_agents.application.agent_prompts import build_system_prompt
from times_of_agents.domain.entities import AgentConfig

logger = logging.getLogger(__name__)


def make_step_callback(agent_name: str) -> Any:
    """Return a CrewAI step_callback that logs every tool call the agent makes."""
    def _callback(step_output: Any) -> None:
        try:
            if isinstance(step_output, dict):
                tool = step_output.get("tool")
                tool_input = step_output.get("tool_input")
            else:
                tool = getattr(step_output, "tool", None)
                tool_input = getattr(step_output, "tool_input", None)

            if tool:
                preview = str(tool_input) if tool_input is not None else ""
                if len(preview) > 120:
                    preview = preview[:120] + "…"
                logger.info("[%s] → tool: %s  %s", agent_name, tool, preview)
        except Exception:
            pass  # never let a logging callback crash the agent
    return _callback


def build_crewai_agent(config: AgentConfig, llm: LLM) -> Agent:
    system_prompt = build_system_prompt(config)

    return Agent(
        role=config.identity.role,
        goal=(
            f"Provide insightful, emotionally authentic analysis of news topics "
            f"from the perspective of a {config.identity.role}. "
            "Engage with peers' arguments, challenge or support them with evidence, "
            "prefer natural paraphrasing over repeated direct quotes, "
            "and always conclude with a concrete implication or open question."
        ),
        backstory=system_prompt,
        llm=llm,
        verbose=False,
        allow_delegation=False,
        memory=False,
        step_callback=make_step_callback(config.identity.name),
    )
