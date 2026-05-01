from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from times_of_agents.application.discussion_orchestrator import run_discussion
from times_of_agents.domain.entities import AgentConfig, AgentIdentity, EmotionProfile

FAKE_RESPONSE = "Sample CrewAI response about the topic."


def _make_task_output(raw: str) -> SimpleNamespace:
    return SimpleNamespace(raw=raw)


def _make_crew_output(n_agents: int) -> SimpleNamespace:
    return SimpleNamespace(
        tasks_output=[_make_task_output(FAKE_RESPONSE) for _ in range(n_agents)]
    )


def _sample_agent(
    agent_id: str,
    *,
    memory_window_messages: int = 8,
    include_topic_every_turn: bool = True,
    temperature: float = 0.7,
) -> AgentConfig:
    return AgentConfig(
        identity=AgentIdentity(
            id=agent_id,
            name=f"Agent {agent_id}",
            role="Analyst",
            description="Testing agent",
        ),
        emotion_profile=EmotionProfile(
            trust=0.7,
            anticipation=0.8,
            joy=0.2,
            surprise=0.3,
            fear=0.4,
            sadness=0.1,
            disgust=0.2,
            anger=0.3,
        ),
        speaking_weight=1.0,
        memory_window_messages=memory_window_messages,
        include_topic_every_turn=include_topic_every_turn,
        temperature=temperature,
    )


@patch("times_of_agents.application.discussion_orchestrator.create_crewai_llm")
@patch("times_of_agents.application.discussion_orchestrator.build_speaking_task")
@patch("times_of_agents.application.discussion_orchestrator.build_crewai_agent")
@patch("times_of_agents.application.discussion_orchestrator.Crew")
def test_run_discussion_message_count(
    mock_crew_cls, mock_build_agent, mock_build_task, mock_llm_factory
) -> None:
    mock_llm_factory.return_value = "anthropic/claude-sonnet-4-5"
    mock_build_agent.return_value = MagicMock()
    mock_build_task.return_value = MagicMock()
    agents = [_sample_agent("a1"), _sample_agent("a2")]
    mock_crew_cls.return_value.kickoff.return_value = _make_crew_output(len(agents))

    result = run_discussion(
        topic="Test topic",
        agent_configs=agents,
        rounds=2,
        seed=7,
        interjections_enabled=False,
    )

    assert result.topic == "Test topic"
    assert result.rounds == 2
    assert len(result.transcript) == 4
    assert all(msg.content == FAKE_RESPONSE for msg in result.transcript)
    assert all(msg.is_interjection is False for msg in result.transcript)


@patch("times_of_agents.application.discussion_orchestrator.create_crewai_llm")
@patch("times_of_agents.application.discussion_orchestrator.build_speaking_task")
@patch("times_of_agents.application.discussion_orchestrator.build_crewai_agent")
@patch("times_of_agents.application.discussion_orchestrator.Crew")
def test_run_discussion_round_indices(
    mock_crew_cls, mock_build_agent, mock_build_task, mock_llm_factory
) -> None:
    mock_llm_factory.return_value = "anthropic/claude-sonnet-4-5"
    mock_build_agent.return_value = MagicMock()
    mock_build_task.return_value = MagicMock()
    agents = [_sample_agent("b1"), _sample_agent("b2")]
    mock_crew_cls.return_value.kickoff.return_value = _make_crew_output(len(agents))

    result = run_discussion(
        topic="Round index test",
        agent_configs=agents,
        rounds=3,
        seed=0,
        interjections_enabled=False,
    )

    assert [msg.round_index for msg in result.transcript] == [1, 1, 2, 2, 3, 3]


@patch("times_of_agents.application.discussion_orchestrator.create_crewai_llm")
@patch("times_of_agents.application.discussion_orchestrator.build_speaking_task")
@patch("times_of_agents.application.discussion_orchestrator.build_crewai_agent")
@patch("times_of_agents.application.discussion_orchestrator.Crew")
def test_run_discussion_emotion_attached(
    mock_crew_cls, mock_build_agent, mock_build_task, mock_llm_factory
) -> None:
    mock_llm_factory.return_value = "anthropic/claude-sonnet-4-5"
    mock_build_agent.return_value = MagicMock()
    mock_build_task.return_value = MagicMock()
    agents = [_sample_agent("c1")]
    mock_crew_cls.return_value.kickoff.return_value = _make_crew_output(1)

    result = run_discussion(
        topic="Emotion test",
        agent_configs=agents,
        rounds=1,
        seed=0,
        interjections_enabled=False,
    )

    assert result.transcript[0].dominant_emotion == "anticipation"


@patch("times_of_agents.application.discussion_orchestrator.create_crewai_llm")
@patch("times_of_agents.application.discussion_orchestrator.Crew")
def test_run_discussion_invalid_rounds(mock_crew_cls, mock_llm_factory) -> None:
    import pytest

    mock_llm_factory.return_value = "anthropic/claude-sonnet-4-5"
    with pytest.raises(ValueError, match="rounds must be positive"):
        run_discussion(
            topic="t",
            agent_configs=[_sample_agent("e1")],
            rounds=0,
            interjections_enabled=False,
        )


@patch("times_of_agents.application.discussion_orchestrator.create_crewai_llm")
@patch("times_of_agents.application.discussion_orchestrator.Crew")
def test_run_discussion_empty_agents(mock_crew_cls, mock_llm_factory) -> None:
    import pytest

    mock_llm_factory.return_value = "anthropic/claude-sonnet-4-5"
    with pytest.raises(ValueError, match="agent_configs must not be empty"):
        run_discussion(
            topic="t",
            agent_configs=[],
            rounds=1,
            interjections_enabled=False,
        )


@patch("times_of_agents.application.discussion_orchestrator.create_crewai_llm")
@patch("times_of_agents.application.discussion_orchestrator.build_speaking_task")
@patch("times_of_agents.application.discussion_orchestrator.build_crewai_agent")
@patch("times_of_agents.application.discussion_orchestrator.Crew")
def test_second_task_receives_prior_context(
    mock_crew_cls, mock_build_agent, mock_build_task, mock_llm_factory
) -> None:
    mock_llm_factory.return_value = "anthropic/claude-sonnet-4-5"
    mock_build_agent.return_value = MagicMock()
    agents = [_sample_agent("d1"), _sample_agent("d2")]
    mock_crew_cls.return_value.kickoff.return_value = _make_crew_output(len(agents))
    mock_build_task.return_value = MagicMock()

    run_discussion(
        topic="Context test",
        agent_configs=agents,
        rounds=1,
        seed=1,
        interjections_enabled=False,
    )

    assert mock_build_task.call_count == 2
    assert mock_build_task.call_args_list[0].kwargs["prior_messages"] == []
    second_prior = mock_build_task.call_args_list[1].kwargs["prior_messages"]
    assert len(second_prior) == 1
    assert second_prior[0].content == FAKE_RESPONSE
    assert mock_build_task.call_args_list[1].kwargs["round_index"] == 1


@patch("times_of_agents.application.discussion_orchestrator.create_crewai_llm")
@patch("times_of_agents.application.discussion_orchestrator.build_speaking_task")
@patch("times_of_agents.application.discussion_orchestrator.build_crewai_agent")
@patch("times_of_agents.application.discussion_orchestrator.Crew")
def test_memory_window_limits_prior_context(
    mock_crew_cls, mock_build_agent, mock_build_task, mock_llm_factory
) -> None:
    mock_llm_factory.return_value = "anthropic/claude-sonnet-4-5"
    mock_build_agent.return_value = MagicMock()
    agents = [_sample_agent("m1", memory_window_messages=0)]
    mock_crew_cls.return_value.kickoff.return_value = _make_crew_output(1)
    mock_build_task.return_value = MagicMock()

    run_discussion(
        topic="Memory window test",
        agent_configs=agents,
        rounds=2,
        seed=1,
        interjections_enabled=False,
    )

    assert mock_build_task.call_count == 2
    assert mock_build_task.call_args_list[0].kwargs["prior_messages"] == []
    assert mock_build_task.call_args_list[1].kwargs["prior_messages"] == []


@patch("times_of_agents.application.discussion_orchestrator.create_crewai_llm")
@patch("times_of_agents.application.discussion_orchestrator.build_speaking_task")
@patch("times_of_agents.application.discussion_orchestrator.build_crewai_agent")
@patch("times_of_agents.application.discussion_orchestrator.Crew")
def test_topic_included_once_when_disabled(
    mock_crew_cls, mock_build_agent, mock_build_task, mock_llm_factory
) -> None:
    mock_llm_factory.return_value = "anthropic/claude-sonnet-4-5"
    mock_build_agent.return_value = MagicMock()
    agents = [_sample_agent("t1", include_topic_every_turn=False)]
    mock_crew_cls.return_value.kickoff.return_value = _make_crew_output(1)
    mock_build_task.return_value = MagicMock()

    run_discussion(
        topic="Topic inclusion test",
        agent_configs=agents,
        rounds=2,
        seed=0,
        interjections_enabled=False,
    )

    assert mock_build_task.call_count == 2
    assert mock_build_task.call_args_list[0].kwargs["include_topic"] is True
    assert mock_build_task.call_args_list[1].kwargs["include_topic"] is False


@patch("times_of_agents.application.discussion_orchestrator.create_crewai_llm")
@patch("times_of_agents.application.discussion_orchestrator.build_speaking_task")
@patch("times_of_agents.application.discussion_orchestrator.build_crewai_agent")
@patch("times_of_agents.application.discussion_orchestrator.Crew")
def test_run_discussion_uses_agent_temperature_for_llm(
    mock_crew_cls, mock_build_agent, mock_build_task, mock_llm_factory
) -> None:
    mock_llm_factory.return_value = "anthropic/claude-sonnet-4-5"
    mock_build_agent.return_value = MagicMock()
    mock_build_task.return_value = MagicMock()
    mock_crew_cls.return_value.kickoff.return_value = _make_crew_output(2)
    agents = [
        _sample_agent("temp1", temperature=0.2),
        _sample_agent("temp2", temperature=1.1),
    ]

    run_discussion(
        topic="Temperature test",
        agent_configs=agents,
        rounds=1,
        seed=0,
        interjections_enabled=False,
    )

    assert mock_llm_factory.call_count == 2
    temperatures = {call.kwargs["temperature"] for call in mock_llm_factory.call_args_list}
    assert temperatures == {0.2, 1.1}
