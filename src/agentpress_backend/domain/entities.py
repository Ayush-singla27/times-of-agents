from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

EMOTION_KEYS: tuple[str, ...] = (
    "trust",
    "anticipation",
    "joy",
    "surprise",
    "fear",
    "sadness",
    "disgust",
    "anger",
)


@dataclass(slots=True)
class EmotionProfile:
    trust: float
    anticipation: float
    joy: float
    surprise: float
    fear: float
    sadness: float
    disgust: float
    anger: float

    def __post_init__(self) -> None:
        for key in EMOTION_KEYS:
            value = getattr(self, key)
            if not 0.0 <= value <= 1.0:
                raise ValueError(f"Emotion '{key}' must be between 0.0 and 1.0, got {value}")

    def dominant_emotion(self) -> str:
        ranked = sorted(self.to_dict().items(), key=lambda kv: kv[1], reverse=True)
        return ranked[0][0]

    def to_dict(self) -> dict[str, float]:
        return {key: getattr(self, key) for key in EMOTION_KEYS}


@dataclass(slots=True)
class AgentIdentity:
    id: str
    name: str
    role: str
    description: str


@dataclass(slots=True)
class AgentConfig:
    identity: AgentIdentity
    emotion_profile: EmotionProfile
    speaking_weight: float = 1.0

    def __post_init__(self) -> None:
        if self.speaking_weight <= 0:
            raise ValueError("speaking_weight must be positive")


@dataclass(slots=True)
class Message:
    round_index: int
    agent_id: str
    agent_name: str
    content: str
    dominant_emotion: str
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))


@dataclass(slots=True)
class TokenUsageSummary:
    call_count: int = 0
    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0
    input_cost_usd: float = 0.0
    output_cost_usd: float = 0.0
    total_cost_usd: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        return {
            "call_count": self.call_count,
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "total_tokens": self.total_tokens,
            "input_cost_usd": round(self.input_cost_usd, 8),
            "output_cost_usd": round(self.output_cost_usd, 8),
            "total_cost_usd": round(self.total_cost_usd, 8),
        }


@dataclass(slots=True)
class DiscussionResult:
    topic: str
    rounds: int
    transcript: list[Message]
    usage_summary: TokenUsageSummary | None = None

    def to_dict(self) -> dict[str, Any]:
        payload = {
            "topic": self.topic,
            "rounds": self.rounds,
            "transcript": [
                {
                    "round_index": msg.round_index,
                    "agent_id": msg.agent_id,
                    "agent_name": msg.agent_name,
                    "content": msg.content,
                    "dominant_emotion": msg.dominant_emotion,
                    "created_at": msg.created_at.isoformat(),
                }
                for msg in self.transcript
            ],
        }
        if self.usage_summary is not None:
            payload["usage_summary"] = self.usage_summary.to_dict()
        return payload
