from __future__ import annotations

from crewai import Agent, Task

from agentpress_backend.domain.entities import Message


def build_speaking_task_prompt(
    *,
    agent_name: str,
    topic: str,
    round_index: int,
    prior_messages: list[Message],
) -> tuple[str, str]:
    context_block = ""
    if prior_messages:
        lines = [
            f"- R{m.round_index} {m.agent_name} ({m.dominant_emotion}): {m.content[:220]}"
            for m in prior_messages[-8:]
        ]
        context_block = (
            "\nPrior discussion context (recent peer comments):\n"
            + "\n".join(lines)
            + "\n"
        )

    description = (
        f"Round {round_index} of the multi-agent news discussion.\n\n"
        f"Topic: {topic}\n"
        f"{context_block}\n"
        "Write one concise comment for this round. "
        "If peer comments are provided, engage with them if you support or disagree,"
        "by naming the agent or quoting the point or provide your unique perspective if you have a different view. "
        "Keep your response under 200 words, focused, and conversational."
    )

    expected_output = (
        "A single focused comment of at most 150 words that: "
        "(1) addresses the news topic through your analytical lens, "
        "(2) references at least one peer statement when prior context exists, "
        "(3) ends with a concrete implication, recommendation, or open question."
    )

    return description, expected_output


def build_speaking_task(
    *,
    agent: Agent,
    agent_name: str,
    topic: str,
    round_index: int,
    prior_messages: list[Message],
) -> Task:
    description, expected_output = build_speaking_task_prompt(
        agent_name=agent_name,
        topic=topic,
        round_index=round_index,
        prior_messages=prior_messages,
    )

    return Task(
        description=description,
        expected_output=expected_output,
        agent=agent,
    )


def build_interjection_task_prompt(
    *,
    agent_name: str,
    topic: str,
    round_index: int,
    prior_messages: list[Message],
    latest_message: Message,
) -> tuple[str, str]:
    context_block = ""
    if prior_messages:
        lines = [
            f"- R{m.round_index} {m.agent_name} ({m.dominant_emotion}): {m.content[:220]}"
            for m in prior_messages[-8:]
        ]
        context_block = (
            "\nPrior discussion context (recent peer comments):\n"
            + "\n".join(lines)
            + "\n"
        )

    description = (
        f"Round {round_index} interjection check.\n\n"
        f"Topic: {topic}\n"
        f"Latest message to react to: {latest_message.agent_name}: {latest_message.content[:240]}\n"
        f"{context_block}\n"
        "If you have a strong opposing argument to the latest message, "
        "write a concise interjection (30-80 words). "
        "If you do NOT have a strong opposing argument, respond with EXACTLY 'NO_INTERJECTION'."
    )

    expected_output = (
        "Either: 'NO_INTERJECTION' exactly, OR a concise interjection that: "
        "(1) directly challenges the latest message with one strong counterpoint, "
        "(2) stays under 80 words, "
        "(3) ends with a concrete implication or open question."
    )

    return description, expected_output


def build_interjection_task(
    *,
    agent: Agent,
    agent_name: str,
    topic: str,
    round_index: int,
    prior_messages: list[Message],
    latest_message: Message,
) -> Task:
    description, expected_output = build_interjection_task_prompt(
        agent_name=agent_name,
        topic=topic,
        round_index=round_index,
        prior_messages=prior_messages,
        latest_message=latest_message,
    )

    return Task(
        description=description,
        expected_output=expected_output,
        agent=agent,
    )
