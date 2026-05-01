from __future__ import annotations

import logging
from pathlib import Path
from typing import Any
from uuid import uuid4

from crewai import Agent, Crew, Process, Task

from times_of_agents.application.usage_tracking import (
    apply_costs,
    collect_usage_from_result,
    estimate_tokens,
    merge_usage,
    resolve_cost_rates,
)
from times_of_agents.domain.entities import TokenUsageSummary
from times_of_agents.infrastructure.llm_factory import create_crewai_llm
from times_of_agents.infrastructure.tavily_search_tool import tavily_search_tool
from times_of_agents.infrastructure.trending_news_tool import (
    NewsArticle,
    fetch_trending_news,
    fetch_trending_news_tool,
    parse_news_payload,
)

logger = logging.getLogger(__name__)


def refresh_topic_from_trending_news(
    *,
    model: str,
    article_count: int = 3,
    articles_dir: Path = Path("data/articles"),
) -> str:
    if article_count <= 0:
        raise ValueError("article_count must be positive")

    llm = create_crewai_llm(model=model, temperature=0.3)
    article_limit = max(article_count * 3, 10)

    collector_agent = Agent(
        role="Trending News Curator",
        goal=f"Fetch trending news and select exactly {article_count} unique articles.",
        backstory=(
            "You are an editorial assistant. Use the fetch_trending_news tool to retrieve stories "
            "and return the best unique ones as a JSON array."
        ),
        llm=llm,
        tools=[fetch_trending_news_tool],
        verbose=False,
        allow_delegation=False,
        max_iter=2,
    )

    task = Task(
        description=(
            f"Call fetch_trending_news once with limit {article_limit}. "
            f"Select {article_count} unique, non-duplicate stories. "
            "Output a JSON array where each item has keys: title, summary, source, link."
        ),
        expected_output=(
            f"A JSON array with exactly {article_count} unique article objects. "
            "Fields: title, summary, source, link."
        ),
        agent=collector_agent,
    )

    crew = Crew(
        agents=[collector_agent],
        tasks=[task],
        process=Process.sequential,
        verbose=False,
        memory=False,
    )

    input_rate, output_rate = resolve_cost_rates()
    usage_summary = TokenUsageSummary()
    used_estimate = False
    curated_articles: list[NewsArticle] = []

    try:
        crew_result = crew.kickoff()
        curated_articles = _extract_articles_from_crew_result(crew_result, expected_count=article_count)
        usage_summary = collect_usage_from_result(crew_result)
        if usage_summary.call_count == 0:
            usage_summary = _estimate_usage_for_task(
                task.description, task.expected_output, _task_raw_output(crew_result)
            )
            used_estimate = True
    except Exception as error:
        logger.warning("News curator agent failed (%s). Using direct feed fallback.", error)

    articles = [_normalize_article(a) for a in curated_articles[:article_count]]

    if len(articles) < article_count:
        needed = article_count - len(articles)
        try:
            fallback_articles = fetch_trending_news(limit=article_limit)
        except Exception as error:
            logger.warning("Could not fetch trending news (%s).", error)
            fallback_articles = _placeholder_articles(article_count)
        articles.extend(_normalize_article(a) for a in fallback_articles[:needed])

    search_summaries, search_usage, search_used_estimate = _generate_search_summaries(
        articles,
        llm=llm,
    )
    merge_usage(usage_summary, search_usage)
    used_estimate = used_estimate or search_used_estimate

    apply_costs(usage_summary, input_rate, output_rate)
    _log_usage_summary(
        usage_summary,
        input_rate=input_rate,
        output_rate=output_rate,
        used_estimate=used_estimate,
    )

    generated_topics = _save_articles_to_files(
        articles,
        articles_dir=articles_dir,
        search_summaries=search_summaries,
    )
    rendered_topic = _render_topic_summary(generated_topics)
    return rendered_topic


def _extract_articles_from_crew_result(crew_result: Any, *, expected_count: int) -> list[NewsArticle]:
    task_outputs = getattr(crew_result, "tasks_output", []) or []
    payload = (getattr(task_outputs[0], "raw", "") or "").strip() if task_outputs else str(crew_result).strip()
    return _dedupe_articles(parse_news_payload(payload))[:expected_count]


def _dedupe_articles(articles: list[NewsArticle]) -> list[NewsArticle]:
    seen_title_keys: set[str] = set()
    seen_links: set[str] = set()
    unique: list[NewsArticle] = []
    for article in articles:
        title_key = " ".join(article.title.lower().split())
        if article.link in seen_links or title_key in seen_title_keys:
            continue
        seen_links.add(article.link)
        seen_title_keys.add(title_key)
        unique.append(article)
    return unique


def _normalize_article(article: NewsArticle) -> NewsArticle:
    description = article.description.strip() or article.summary.strip()
    summary = article.summary.strip() or description
    return NewsArticle(
        title=article.title,
        summary=summary,
        link=article.link,
        source=article.source,
        cause=article.cause.strip(),
        description=description,
        key_points=article.key_points.strip(),
        implications=article.implications.strip(),
        stakeholders=article.stakeholders.strip(),
    )


def _save_articles_to_files(
    articles: list[NewsArticle],
    *,
    articles_dir: Path,
    search_summaries: list[str] | None = None,
) -> list[tuple[str, NewsArticle, Path]]:
    articles_dir.mkdir(parents=True, exist_ok=True)

    for stale_file in articles_dir.glob("*.txt"):
        stale_file.unlink()

    summaries = _normalize_search_summaries(articles, search_summaries)

    generated: list[tuple[str, NewsArticle, Path]] = []
    for idx, article in enumerate(articles, start=1):
        topic_id = f"topic-{uuid4().hex[:8]}"
        filename = articles_dir / f"{idx:02d}_{topic_id}_{_sanitize_filename(article.title)}.txt"
        summary_text = summaries[idx - 1]
        content = (
            f"Title: {article.title}\n"
            f"Topic ID: {topic_id}\n"
            f"Source: {article.source}\n"
            f"Link: {article.link}\n\n"
            f"Description:\n{article.description}\n\n"
            f"Search Summary (approx. 500 words):\n{summary_text}\n"
        )
        filename.write_text(content, encoding="utf-8")
        generated.append((topic_id, article, filename))

    return generated


def _sanitize_filename(title: str) -> str:
    sanitized = "".join(c if c.isalnum() or c in " _-" else "" for c in title)
    slugified = "_".join(sanitized.split()[:5])
    return slugified[:50]


def _render_topic_summary(generated_topics: list[tuple[str, NewsArticle, Path]]) -> str:
    lines = ["Topics for discussion (use --topic-id):"]
    for idx, (topic_id, article, _path) in enumerate(generated_topics, start=1):
        lines.append(f"{idx}. [{topic_id}] {article.title}")
    return "\n".join(lines)


def _placeholder_articles(article_count: int) -> list[NewsArticle]:
    return [
        NewsArticle(
            title=f"Live news temporarily unavailable ({idx})",
            summary="Could not fetch trending stories due to a network or SSL issue.",
            link="https://news.google.com/",
            source="System",
            description="News feed unavailable. Please retry later.",
        )
        for idx in range(1, article_count + 1)
    ]


def _task_raw_output(crew_result: Any, task_index: int = 0) -> str:
    task_outputs = getattr(crew_result, "tasks_output", []) or []
    if task_outputs:
        if 0 <= task_index < len(task_outputs):
            return (getattr(task_outputs[task_index], "raw", "") or "").strip()
        return ""
    return str(crew_result).strip() if task_index == 0 else ""


def _estimate_usage_for_task(description: str, expected_output: str, raw_content: str) -> TokenUsageSummary:
    prompt_text = description + "\n\n" + expected_output
    summary = TokenUsageSummary(call_count=1)
    summary.input_tokens = estimate_tokens(prompt_text)
    summary.output_tokens = estimate_tokens(raw_content)
    summary.total_tokens = summary.input_tokens + summary.output_tokens
    return summary


def _generate_search_summaries(
    articles: list[NewsArticle],
    *,
    llm: Any,
    max_results: int = 5,
) -> tuple[list[str], TokenUsageSummary, bool]:
    if not articles:
        return [], TokenUsageSummary(), False

    researcher_agent = Agent(
        role="News Research Analyst",
        goal="Search for each topic and write an approximately 500-word summary.",
        backstory=(
            "You quickly review web results and synthesize a neutral, factual summary. "
            "Use the search_tavily tool to gather context before writing."
        ),
        llm=llm,
        tools=[tavily_search_tool],
        verbose=False,
        allow_delegation=False,
        max_iter=2,
    )

    tasks: list[Task] = []
    for article in articles:
        tasks.append(
            Task(
                description=(
                    "Call search_tavily with query: "
                    f"\"{article.title}\" and max_results {max_results}. "
                    "Then write a concise, neutral summary of the topic in 450-550 words. "
                    "Focus on the main facts, recent developments, and key stakeholders."
                ),
                expected_output="A 450-550 word summary with no bullet lists or citations.",
                agent=researcher_agent,
            )
        )

    crew = Crew(
        agents=[researcher_agent],
        tasks=tasks,
        process=Process.sequential,
        verbose=False,
        memory=False,
    )

    usage_summary = TokenUsageSummary()
    used_estimate = False
    summaries: list[str] = []

    try:
        crew_result = crew.kickoff()
        for idx, article in enumerate(articles):
            raw_summary = _task_raw_output(crew_result, task_index=idx)
            summaries.append(_prepare_search_summary(raw_summary, article))

        usage_summary = collect_usage_from_result(crew_result)
        if usage_summary.call_count == 0:
            for idx, task in enumerate(tasks):
                estimate = _estimate_usage_for_task(
                    task.description,
                    task.expected_output,
                    _task_raw_output(crew_result, task_index=idx),
                )
                merge_usage(usage_summary, estimate)
            used_estimate = True
    except Exception as error:
        logger.warning("Tavily search summary failed (%s). Using article summaries.", error)
        summaries = [_prepare_search_summary("", article) for article in articles]

    return summaries, usage_summary, used_estimate


def _prepare_search_summary(summary: str, article: NewsArticle) -> str:
    cleaned = summary.strip()
    if cleaned:
        return _trim_summary(cleaned)

    fallback = (article.summary or article.description or "").strip()
    if fallback:
        return _trim_summary(fallback)

    return "Search summary unavailable."


def _trim_summary(summary: str, max_words: int = 520) -> str:
    words = summary.split()
    if len(words) <= max_words:
        return summary
    return " ".join(words[:max_words]).rstrip() + "..."


def _normalize_search_summaries(articles: list[NewsArticle], summaries: list[str] | None) -> list[str]:
    if summaries is None:
        summaries = []
    normalized: list[str] = []
    for idx, article in enumerate(articles):
        summary = summaries[idx] if idx < len(summaries) else ""
        normalized.append(_prepare_search_summary(summary, article))
    return normalized


def _log_usage_summary(
    summary: TokenUsageSummary,
    *,
    input_rate: float,
    output_rate: float,
    used_estimate: bool,
) -> None:
    estimate_note = " (estimated)" if used_estimate else ""
    logger.info(
        "News topic token usage%s: input=%s, output=%s, total=%s, calls=%s",
        estimate_note,
        summary.input_tokens,
        summary.output_tokens,
        summary.total_tokens,
        summary.call_count,
    )
    if input_rate == 0.0 and output_rate == 0.0:
        logger.info(
            "News topic token cost: $0.000000 (set TOKEN_INPUT_COST_PER_1K_USD and "
            "TOKEN_OUTPUT_COST_PER_1K_USD to enable cost estimation)"
        )
        return

    logger.info(
        "News topic token cost: $%.6f (input $%.6f + output $%.6f, rates: $%.4f/$%.4f per 1K)",
        summary.total_cost_usd,
        summary.input_cost_usd,
        summary.output_cost_usd,
        input_rate,
        output_rate,
    )

