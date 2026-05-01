from __future__ import annotations

import argparse
import logging
from pathlib import Path

from times_of_agents.application.discussion_orchestrator import run_discussion
from times_of_agents.application.news_topic_agent import refresh_topic_from_trending_news
from times_of_agents.infrastructure.agent_config_file import load_agent_configs
from times_of_agents.infrastructure.result_file_writer import write_result_json
from times_of_agents.infrastructure.topic_file import load_topic

DEFAULT_TOPIC_FILE = Path("data/topic.txt")
DEFAULT_AGENT_CONFIG_FILE = Path("data/agents.json")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="times-of-agents",
        description="Run news generation and/or multi-agent discussion.",
    )
    parser.add_argument("--topic-file", type=Path, default=DEFAULT_TOPIC_FILE, help="Path to topic file")
    parser.add_argument(
        "--topic",
        type=str,
        default=None,
        help="Optional topic text for discussion mode (bypasses topic file)",
    )
    parser.add_argument(
        "--agent-config-file",
        type=Path,
        default=DEFAULT_AGENT_CONFIG_FILE,
        help="Path to JSON agent config",
    )
    parser.add_argument("--rounds", type=int, default=3, help="Number of discussion rounds")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for agent ordering")
    parser.add_argument(
        "--model",
        type=str,
        default="gpt-4o-mini",
        help="Model ID (for example: gpt-4o-mini or openai/gpt-4o-mini)",
    )
    parser.add_argument(
        "--news-article-count",
        type=int,
        default=3,
        help="How many trending news items to curate into the topic file",
    )
    parser.add_argument(
        "--generate-news-topic",
        dest="generate_news_topic",
        action="store_true",
        help="Generate trending news articles and save each to a separate file in data/articles/",
    )
    parser.add_argument(
        "--agent-discussion",
        action="store_true",
        help="Run agent discussion using --topic or --topic-file",
    )
    parser.add_argument("--output-file", type=Path, default=None, help="Optional output transcript JSON path")
    parser.add_argument("--log-level", default="INFO", choices=["DEBUG", "INFO", "WARNING", "ERROR"])
    parser.add_argument(
        "--topic-id",
        type=str,
        default=None,
        help="Topic identifier from generated files (for example: topic-1a2b3c4d)",
    )
    return parser


def _resolve_run_modes(args: argparse.Namespace) -> tuple[bool, bool]:
    generate_news_topic = bool(args.generate_news_topic)
    run_agent_discussion = bool(args.agent_discussion)

    if not generate_news_topic and not run_agent_discussion:
        return True, True

    return generate_news_topic, run_agent_discussion


def _load_topic_from_articles_or_file(topic_file: Path) -> str:
    """Load topic from individual article files or fall back to topic file."""
    articles_dir = Path("data/articles")
    if articles_dir.exists():
        article_files = sorted(articles_dir.glob("*.txt"))
        if article_files:
            titles = []
            for f in article_files:
                lines = f.read_text(encoding="utf-8").splitlines()
                title = lines[0].strip() if lines else f.stem
                topic_id = ""
                for line in lines[1:4]:
                    if line.startswith("Topic ID:"):
                        topic_id = line.split(":", 1)[1].strip()
                        break
                topic_label = f"[{topic_id}] " if topic_id else ""
                titles.append(f"{topic_label}{title}")
            return "Topics for discussion:\n" + "\n".join(f"{i}. {t}" for i, t in enumerate(titles, 1))
    return load_topic(topic_file)


def _load_topic_by_id(topic_id: str, *, articles_dir: Path = Path("data/articles")) -> str:
    normalized = topic_id.strip()
    if not normalized:
        raise ValueError("--topic-id cannot be empty")

    for article_file in sorted(articles_dir.glob("*.txt")):
        lines = article_file.read_text(encoding="utf-8").splitlines()
        if any(line.strip() == f"Topic ID: {normalized}" for line in lines[:6]):
            return "\n".join(lines).strip()

    raise FileNotFoundError(
        f"Topic ID not found: {normalized}. Generate topics first with --generate-news-topic."
    )


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    logging.basicConfig(
        level=getattr(logging, args.log_level),
        format="%(asctime)s %(levelname)s %(name)s - %(message)s",
    )
    logger = logging.getLogger("times-of-agents")

    logger.info("Initializing Times of Agents...")
    logger.info("Model: %s", args.model)
    logger.info("Note: Ensure the matching provider API key is set (for GPT models, OPENAI_API_KEY)")

    generate_news_topic, run_agent_discussion = _resolve_run_modes(args)
    generated_topic: str | None = None

    if generate_news_topic:
        logger.info(
            "Generating %d trending news articles into data/articles/",
            args.news_article_count,
        )
        generated_topic = refresh_topic_from_trending_news(
            model=args.model,
            article_count=args.news_article_count,
        )
        logger.info("News generation complete")

    if not run_agent_discussion:
        return

    if args.topic and args.topic_id:
        raise ValueError("Use either --topic or --topic-id, not both")

    if args.topic:
        topic = args.topic.strip()
        if not topic:
            raise ValueError("--topic cannot be empty")
    elif args.topic_id:
        topic = _load_topic_by_id(args.topic_id)
    elif generated_topic is not None:
        topic = generated_topic
    else:
        topic = _load_topic_from_articles_or_file(args.topic_file)

    agent_configs = load_agent_configs(args.agent_config_file)
    agent_configs_by_id = {cfg.identity.id: cfg for cfg in agent_configs}

    result = run_discussion(
        topic=topic,
        agent_configs=agent_configs,
        rounds=args.rounds,
        seed=args.seed,
        model=args.model,
    )

    logger.info("Topic: %s", result.topic)
    logger.info("Rounds: %d", result.rounds)
    logger.info("Messages generated: %d", len(result.transcript))

    for msg in result.transcript:
        message_kind = "INTERJECTION" if msg.is_interjection else "STATEMENT"
        agent_cfg = agent_configs_by_id.get(msg.agent_id)
        memory_info = ""
        if agent_cfg is not None:
            memory_info = (
                f" [memory_window_messages={agent_cfg.memory_window_messages}, "
                f"include_topic_every_turn={agent_cfg.include_topic_every_turn}, "
                f"temperature={agent_cfg.temperature}]"
            )
        print(
            f"[R{msg.round_index}] [{message_kind}] {msg.agent_name} ({msg.dominant_emotion})"
            f"{memory_info}:\n{msg.content}\n"
        )

    if args.output_file is not None:
        write_result_json(result=result, output_path=args.output_file)
        logger.info("Wrote discussion JSON to %s", args.output_file)


if __name__ == "__main__":
    main()
