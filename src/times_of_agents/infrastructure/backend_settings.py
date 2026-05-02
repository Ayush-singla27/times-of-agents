from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

DEFAULT_CONFIG_FILE = Path("data/backend_config.json")


@dataclass(slots=True)
class BackendSettings:
    db_path: Path = Path("data/times_of_agents.db")
    agents_config_file: Path = Path("data/agents.json")
    articles_dir: Path = Path("data/articles")
    model: str = "gpt-4o-mini"
    article_count: int = 3
    rounds: int = 2
    seed: int = 42
    schedule_hour_utc: int = 5
    run_on_startup: bool = True
    enable_scheduler: bool = True
    write_articles_to_files: bool = False
    discussions_per_run: int = 1
    token_input_cost_per_1k_usd: float = 0.0
    token_output_cost_per_1k_usd: float = 0.0

    @classmethod
    def from_config_file(cls, config_file: Path | None = None) -> BackendSettings:
        defaults = cls()
        target_file = (config_file or DEFAULT_CONFIG_FILE).expanduser()

        payload: dict[str, Any] = {}
        if target_file.exists():
            with target_file.open("r", encoding="utf-8") as config_stream:
                loaded_payload = json.load(config_stream)
            if not isinstance(loaded_payload, dict):
                raise ValueError("Backend config must be a JSON object")
            payload = loaded_payload

        base_dir = target_file.parent
        settings = cls(
            db_path=_resolve_path(payload.get("db_path"), defaults.db_path, base_dir),
            agents_config_file=_resolve_path(
                payload.get("agents_config_file"), defaults.agents_config_file, base_dir
            ),
            articles_dir=_resolve_path(payload.get("articles_dir"), defaults.articles_dir, base_dir),
            model=_parse_str(payload.get("model"), defaults.model),
            article_count=_parse_int(payload.get("article_count"), defaults.article_count, "article_count"),
            rounds=_parse_int(payload.get("rounds"), defaults.rounds, "rounds"),
            seed=_parse_int(payload.get("seed"), defaults.seed, "seed"),
            schedule_hour_utc=_parse_int(
                payload.get("schedule_hour_utc"),
                defaults.schedule_hour_utc,
                "schedule_hour_utc",
            ),
            run_on_startup=_parse_bool(payload.get("run_on_startup"), defaults.run_on_startup, "run_on_startup"),
            enable_scheduler=_parse_bool(
                payload.get("enable_scheduler"),
                defaults.enable_scheduler,
                "enable_scheduler",
            ),
            write_articles_to_files=_parse_bool(
                payload.get("write_articles_to_files"),
                defaults.write_articles_to_files,
                "write_articles_to_files",
            ),
            discussions_per_run=_parse_int(
                payload.get("discussions_per_run"),
                defaults.discussions_per_run,
                "discussions_per_run",
            ),
            token_input_cost_per_1k_usd=_parse_float(
                payload.get("token_input_cost_per_1k_usd"),
                defaults.token_input_cost_per_1k_usd,
                "token_input_cost_per_1k_usd",
            ),
            token_output_cost_per_1k_usd=_parse_float(
                payload.get("token_output_cost_per_1k_usd"),
                defaults.token_output_cost_per_1k_usd,
                "token_output_cost_per_1k_usd",
            ),
        )
        settings._validate()
        return settings

    # Backward-compatible alias for older call sites.
    @classmethod
    def from_env(cls) -> BackendSettings:
        return cls.from_config_file()

    def _validate(self) -> None:
        if not 0 <= self.schedule_hour_utc <= 23:
            raise ValueError("schedule_hour_utc must be between 0 and 23")
        if self.article_count <= 0:
            raise ValueError("article_count must be positive")
        if self.rounds <= 0:
            raise ValueError("rounds must be positive")
        if self.discussions_per_run <= 0:
            raise ValueError("discussions_per_run must be positive")


_cached_settings: BackendSettings | None = None
_cached_config_path: Path | None = None


def load_backend_settings(
    config_file: Path | None = None,
    *,
    force_reload: bool = False,
) -> BackendSettings:
    global _cached_settings, _cached_config_path

    target_file = (config_file or DEFAULT_CONFIG_FILE).expanduser().resolve()
    if force_reload or _cached_settings is None or _cached_config_path != target_file:
        _cached_settings = BackendSettings.from_config_file(target_file)
        _cached_config_path = target_file
    return _cached_settings


def get_backend_settings() -> BackendSettings:
    return load_backend_settings()


def _resolve_path(value: object, default: Path, base_dir: Path) -> Path:
    if value is None:
        return default
    if not isinstance(value, str):
        raise ValueError("Path values must be strings")
    parsed = Path(value).expanduser()
    if parsed.is_absolute():
        return parsed
    return (base_dir / parsed).resolve()


def _parse_str(value: object, default: str) -> str:
    if value is None:
        return default
    if not isinstance(value, str):
        raise ValueError("Expected string value")
    return value


def _parse_int(value: object, default: int, field_name: str) -> int:
    if value is None:
        return default
    if isinstance(value, bool):
        raise ValueError(f"{field_name} must be an integer")
    if isinstance(value, (int, float, str)):
        try:
            return int(value)
        except ValueError as error:
            raise ValueError(f"{field_name} must be an integer") from error
    raise ValueError(f"{field_name} must be an integer")


def _parse_float(value: object, default: float, field_name: str) -> float:
    if value is None:
        return default
    if isinstance(value, bool):
        raise ValueError(f"{field_name} must be a number")
    if isinstance(value, (int, float, str)):
        try:
            return float(value)
        except ValueError as error:
            raise ValueError(f"{field_name} must be a number") from error
    raise ValueError(f"{field_name} must be a number")


def _parse_bool(value: object, default: bool, field_name: str) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(value)
    if isinstance(value, str):
        normalized = value.strip().lower()
        if normalized in {"1", "true", "yes", "on"}:
            return True
        if normalized in {"0", "false", "no", "off"}:
            return False
    raise ValueError(f"{field_name} must be a boolean")
