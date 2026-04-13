from __future__ import annotations

from crewai import Agent, LLM

from times_of_agents.application.agent_runtime import build_system_prompt
from times_of_agents.domain.entities import AgentConfig


def build_crewai_agent(config: AgentConfig, llm: LLM) -> Agent:
    system_prompt = build_system_prompt(config)

    return Agent(
        role=config.identity.role,
        goal=(
            f"Provide insightful, emotionally authentic analysis of news topics "
            f"from the perspective of a {config.identity.role}. "
            "Engage with peers' arguments, challenge or support them with evidence, "
            "and always conclude with a concrete implication or open question."
        ),
        backstory=system_prompt,
        llm=llm,
        verbose=True,
        allow_delegation=False,
        memory=False,
    )
