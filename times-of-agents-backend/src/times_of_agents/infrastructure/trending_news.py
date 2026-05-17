from __future__ import annotations

import dataclasses
import json
import re
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from difflib import SequenceMatcher
from html import unescape
from json import JSONDecodeError
from typing import Any

import requests
from crewai.tools import tool

_GOOGLE_NEWS_RSS = "https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en"
_HTML_TAG_RE = re.compile(r"<[^>]+>")
_NON_ALNUM_RE = re.compile(r"[^a-z0-9]+")

@dataclass(frozen=True)
class NewsArticle:
    title: str
    summary: str
    link: str
    source: str
    cause: str = ""
    description: str = ""
    key_points: str = ""
    implications: str = ""
    stakeholders: str = ""


@tool("fetch_trending_news")
def fetch_trending_news_tool(limit: int = 10) -> str:
    """Fetch trending news as JSON for CrewAI agents."""
    articles = fetch_trending_news(limit=limit)
    return json.dumps([dataclasses.asdict(article) for article in articles], ensure_ascii=True)


def fetch_trending_news(limit: int = 10) -> list[NewsArticle]:
    if limit <= 0:
        raise ValueError("limit must be positive")

    try:
        response = requests.get(
            _GOOGLE_NEWS_RSS,
            headers={"User-Agent": "times-of-agents/1.0"},
            timeout=15,
        )
        response.raise_for_status()
    except requests.RequestException as error:
        raise RuntimeError("Failed to fetch trending news feed") from error

    root = ET.fromstring(response.content)
    raw_items: list[NewsArticle] = []
    for item in root.findall("./channel/item"):
        title = _clean_text(item.findtext("title", default=""))
        description = _clean_text(item.findtext("description", default=""))
        link = item.findtext("link", default="").strip()
        source = _clean_text(item.findtext("source", default="Google News")) or "Google News"
        if not title or not link:
            continue
        raw_items.append(
            NewsArticle(
                title=title,
                summary=description,
                link=link,
                source=source,
            )
        )

    unique_articles: list[NewsArticle] = []
    for candidate in raw_items:
        if any(_is_duplicate(candidate, existing) for existing in unique_articles):
            continue
        unique_articles.append(candidate)
        if len(unique_articles) >= limit:
            break

    return unique_articles


def _clean_text(value: str) -> str:
    text = unescape(_HTML_TAG_RE.sub(" ", value)).strip()
    return re.sub(r"\s+", " ", text)


def _normalized(value: str) -> str:
    return _NON_ALNUM_RE.sub(" ", value.lower()).strip()


def _token_set(value: str) -> set[str]:
    return set(_NON_ALNUM_RE.sub(" ", value.lower()).split())


def _jaccard_similarity(a: set[str], b: set[str]) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def _is_duplicate(candidate: NewsArticle, existing: NewsArticle) -> bool:
    if candidate.link and candidate.link == existing.link:
        return True

    title_ratio = SequenceMatcher(
        None,
        _normalized(candidate.title),
        _normalized(existing.title),
    ).ratio()
    if title_ratio >= 0.9:
        return True

    title_overlap = _jaccard_similarity(_token_set(candidate.title), _token_set(existing.title))
    summary_overlap = _jaccard_similarity(
        _token_set(candidate.summary),
        _token_set(existing.summary),
    )
    return title_overlap >= 0.75 and summary_overlap >= 0.7


def parse_news_payload(payload: str) -> list[NewsArticle]:
    try:
        parsed: Any = json.loads(payload)
    except JSONDecodeError:
        return []

    if not isinstance(parsed, list):
        return []

    articles: list[NewsArticle] = []
    for item in parsed:
        if not isinstance(item, dict):
            continue
        title = str(item.get("title", "")).strip()
        summary = str(item.get("summary", "")).strip()
        description = str(item.get("description", "")).strip()
        cause = str(item.get("cause", "")).strip()
        key_points_raw = item.get("key_points", "")
        implications_raw = item.get("implications", "")
        stakeholders_raw = item.get("stakeholders", "")

        key_points = (
            "\n".join(str(point).strip() for point in key_points_raw if str(point).strip())
            if isinstance(key_points_raw, list)
            else str(key_points_raw).strip()
        )
        implications = (
            "\n".join(str(point).strip() for point in implications_raw if str(point).strip())
            if isinstance(implications_raw, list)
            else str(implications_raw).strip()
        )
        stakeholders = (
            ", ".join(str(actor).strip() for actor in stakeholders_raw if str(actor).strip())
            if isinstance(stakeholders_raw, list)
            else str(stakeholders_raw).strip()
        )

        link = str(item.get("link", "")).strip()
        source = str(item.get("source", "")).strip() or "Google News"
        if not title or not link:
            continue

        if not summary and description:
            summary = description
        if not description and summary:
            description = summary

        articles.append(
            NewsArticle(
                title=title,
                summary=summary,
                link=link,
                source=source,
                cause=cause,
                description=description,
                key_points=key_points,
                implications=implications,
                stakeholders=stakeholders,
            )
        )
    return articles

