from __future__ import annotations

import argparse
import logging
from pathlib import Path

from times_of_agents.application.discussion_orchestrator import run_discussion
from times_of_agents.infrastructure.agent_config_file import load_agent_configs
from times_of_agents.infrastructure.result_file_writer import write_result_json
from times_of_agents.infrastructure.topic_file import load_topic

DEFAULT_TOPIC_FILE = Path("data/topic.txt")
DEFAULT_AGENT_CONFIG_FILE = Path("data/agents.json")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="times-of-agents",
        description="Run a CLI multi-agent LLM discussion on a local news topic.",
    )
    parser.add_argument("--topic-file", type=Path, default=DEFAULT_TOPIC_FILE, help="Path to topic file")
    parser.add_argument(
        "--agent-config-file",
        type=Path,
        default=DEFAULT_AGENT_CONFIG_FILE,
        help="Path to JSON agent config",
    )
    parser.add_argument("--rounds", type=int, default=3, help="Number of discussion rounds")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for agent ordering")
    parser.add_argument("--model", type=str, default="claude-sonnet-4-5", help="Claude model ID")
    parser.add_argument("--output-file", type=Path, default=None, help="Optional output transcript JSON path")
    parser.add_argument("--log-level", default="INFO", choices=["DEBUG", "INFO", "WARNING", "ERROR"])
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    logging.basicConfig(
        level=getattr(logging, args.log_level),
        format="%(asctime)s %(levelname)s %(name)s - %(message)s",
    )
    logger = logging.getLogger("times-of-agents")

    logger.info("Initializing multi-agent discussion (LLM-powered)...")
    logger.info("Model: %s", args.model)
    logger.info("Note: Ensure ANTHROPIC_API_KEY environment variable is set")

    result = run_discussion(
        topic=load_topic(args.topic_file),
        agent_configs=load_agent_configs(args.agent_config_file),
        rounds=args.rounds,
        seed=args.seed,
        model=args.model,
    )

    logger.info("Topic: %s", result.topic)
    logger.info("Rounds: %d", result.rounds)
    logger.info("Messages generated: %d", len(result.transcript))

    for msg in result.transcript:
        print(f"[R{msg.round_index}] {msg.agent_name} ({msg.dominant_emotion}):\n{msg.content}\n")

    if args.output_file is not None:
        write_result_json(result=result, output_path=args.output_file)
        logger.info("Wrote discussion JSON to %s", args.output_file)


if __name__ == "__main__":
    main()
