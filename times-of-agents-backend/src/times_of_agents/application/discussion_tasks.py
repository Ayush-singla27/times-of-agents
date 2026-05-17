from __future__ import annotations

from crewai import Agent, Task

from times_of_agents.domain.entities import Message


def _build_context_block(prior_messages: list[Message]) -> str:
    if not prior_messages:
        return ""
    lines = [f"- {m.agent_name}: {m.content[:400]}" for m in prior_messages]
    return "\nConversation so far:\n" + "\n".join(lines) + "\n"


def build_speaking_task_prompt(
    *,
    topic: str,
    round_index: int,
    prior_messages: list[Message],
    include_topic: bool,
) -> tuple[str, str]:
    context_block = _build_context_block(prior_messages)
    topic_line = f"Topic: {topic}\n" if include_topic else ""

    description = (
        f"Round {round_index}.\n\n"
        f"{topic_line}"
        f"{context_block}"
        "\n"
        "Write 1–2 sentences. That is your response. Nothing more unless you have a genuinely "
        "multi-step argument (maximum 4 sentences absolute hard limit).\n\n"
        "Do not restate the topic. Do not summarise what was just said. No filler."
    )

    expected_output = (
        "1–2 sentences. Hard limit is 4 sentences. No exceptions."
    )

    return description, expected_output


def build_speaking_task(
    *,
    agent: Agent,
    topic: str,
    round_index: int,
    prior_messages: list[Message],
    include_topic: bool,
) -> Task:
    description, expected_output = build_speaking_task_prompt(
        topic=topic,
        round_index=round_index,
        prior_messages=prior_messages,
        include_topic=include_topic,
    )

    return Task(
        description=description,
        expected_output=expected_output,
        agent=agent,
    )


def build_interjection_task_prompt(
    *,
    topic: str,
    round_index: int,
    prior_messages: list[Message],
    latest_message: Message,
    include_topic: bool,
) -> tuple[str, str]:
    context_block = _build_context_block(prior_messages)
    topic_line = f"Topic: {topic}\n" if include_topic else ""

    description = (
        f"Round {round_index} — interjection check.\n\n"
        f"{topic_line}"
        f"{latest_message.agent_name} just said: {latest_message.content[:400]}\n"
        f"{context_block}"
        "\n"
        "Do you have something sharp to say back — a direct challenge, a contradiction, or a correction "
        "to a specific claim they just made?\n\n"
        "If yes: write your interjection. It can be as short as one blunt sentence or up to ~60 words. "
        "Don't restate the topic. Don't pad. Just the pushback.\n\n"
        "If you don't have a genuine strong reaction to THIS specific message, respond with exactly: NO_INTERJECTION"
    )

    expected_output = (
        "Either 'NO_INTERJECTION' (exactly), or a direct, unpadded reaction to the latest message — "
        "one sharp sentence up to ~60 words. No topic restatement, no openers, no filler."
    )

    return description, expected_output


def build_interjection_task(
    *,
    agent: Agent,
    topic: str,
    round_index: int,
    prior_messages: list[Message],
    latest_message: Message,
    include_topic: bool,
) -> Task:
    description, expected_output = build_interjection_task_prompt(
        topic=topic,
        round_index=round_index,
        prior_messages=prior_messages,
        latest_message=latest_message,
        include_topic=include_topic,
    )

    return Task(
        description=description,
        expected_output=expected_output,
        agent=agent,
    )
