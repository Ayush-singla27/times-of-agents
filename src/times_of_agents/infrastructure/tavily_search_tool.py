from __future__ import annotations

from dataclasses import dataclass
import json
import os
from typing import Any

import requests
from crewai.tools import tool

_TAVILY_API_URL = "https://api.tavily.com/search"


@dataclass(frozen=True)
class TavilyResult:
    title: str
    url: str
    content: str
    score: float
    published_date: str = ""


@tool("search_tavily")
def tavily_search_tool(query: str, max_results: int = 5, search_depth: str = "basic") -> str:
    """Search the internet with Tavily and return JSON for CrewAI agents."""
    results = search_tavily(query=query, max_results=max_results, search_depth=search_depth)
    return json.dumps([result.__dict__ for result in results], ensure_ascii=True)


def search_tavily(query: str, max_results: int = 5, search_depth: str = "basic") -> list[TavilyResult]:
    if not query.strip():
        raise ValueError("query must be provided")
    if max_results <= 0:
        raise ValueError("max_results must be positive")

    api_key = _require_api_key()
    payload = {
        "api_key": api_key,
        "query": query,
        "search_depth": search_depth,
        "max_results": max_results,
        "include_answer": False,
        "include_raw_content": False,
    }

    try:
        response = requests.post(
            _TAVILY_API_URL,
            json=payload,
            headers={"User-Agent": "times-of-agents/1.0"},
            timeout=20,
        )
        response.raise_for_status()
    except requests.RequestException as error:
        raise RuntimeError("Failed to fetch Tavily search results") from error

    try:
        data: Any = response.json()
    except ValueError as error:
        raise RuntimeError("Invalid Tavily response payload") from error

    raw_results = data.get("results", []) if isinstance(data, dict) else []
    results: list[TavilyResult] = []
    for item in raw_results:
        if not isinstance(item, dict):
            continue
        title = str(item.get("title", "")).strip()
        url = str(item.get("url", "")).strip()
        content = str(item.get("content", "")).strip()
        score = float(item.get("score", 0.0) or 0.0)
        published_date = str(item.get("published_date", "")).strip()
        if not title or not url:
            continue
        results.append(
            TavilyResult(
                title=title,
                url=url,
                content=content,
                score=score,
                published_date=published_date,
            )
        )

    return results


def _require_api_key() -> str:
    api_key = os.getenv("TAVILY_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("TAVILY_API_KEY is required to use Tavily search")
    return api_key
