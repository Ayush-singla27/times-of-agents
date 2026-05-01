from __future__ import annotations

from crewai import Agent, Task

from times_of_agents.domain.entities import Message


def _build_context_block(prior_messages: list[Message]) -> str:
    if not prior_messages:
        return ""
    lines = [f"- R{m.round_index} {m.agent_name} ({m.dominant_emotion}): {m.content[:220]}" for m in prior_messages]
    return "\nPrior discussion context (recent peer comments):\n" + "\n".join(lines) + "\n"


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
        f"Round {round_index} of the multi-agent news discussion.\n\n"
        f"{topic_line}"
        f"{context_block}"
        "\n"
        "Write one concise comment for this round as part of an ongoing conversation, not a standalone essay. "
        "If peer comments are provided, begin by responding to one concrete point from the latest context (support, refine, or challenge). "
        "You do not need to restate the full topic each turn; focus on advancing the dialogue. "
        "Quote exact wording only occasionally when it is essential (max one short quote). "
        "Prefer fresh phrasing and synthesis over reusing lines from the topic text. "
        "Start with your interpretation, consequence, or a probing question; avoid opening with a repeated person-name headline fragment. "
        "Keep your response under 200 words, focused, and conversational."
    )

    expected_output = (
        "A single focused comment of at most 150 words that: "
        "(1) addresses the discussion through your analytical lens, "
        "(2) directly responds to at least one recent peer point when prior context exists (mainly via paraphrase), "
        "(3) uses at most one short direct quote when wording is critical, "
        "(4) opens with a fresh framing instead of a repeated headline-style opener, "
        "(5) advances the conversation with a concrete implication, recommendation, or open question."
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
        f"Round {round_index} interjection check.\n\n"
        f"{topic_line}"
        f"Latest message to react to: {latest_message.agent_name}: {latest_message.content[:240]}\n"
        f"{context_block}"
        "\n"
        "If you have a strong opposing argument to the latest message, "
        "write a concise interjection (30-80 words) that directly challenges a specific claim in that message. "
        "Do not restate the full topic background. "
        "Prefer paraphrasing over quoting, and if you quote, keep it to one short phrase. "
        "Open with a fresh counterpoint, not a repeated headline-style opener. "
        "If you do NOT have a strong opposing argument, respond with EXACTLY 'NO_INTERJECTION'."
    )

    expected_output = (
        "Either: 'NO_INTERJECTION' exactly, OR a concise interjection that: "
        "(1) directly challenges a specific point from the latest message with one strong counterpoint, "
        "(2) stays under 80 words, "
        "(3) mostly paraphrases (with at most one short quote when essential), "
        "(4) ends with a concrete implication or open question."
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
