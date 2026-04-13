from __future__ import annotations

import json
from pathlib import Path

from agentpress_backend.domain.entities import DiscussionResult


def write_result_json(result: DiscussionResult, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result.to_dict(), indent=2), encoding="utf-8")
