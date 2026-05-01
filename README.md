# AgentPress Backend (CLI)

An agentic Python backend for a multi-agent news discussion system powered by **CrewAI**.

## What This Base Includes

- CrewAI-orchestrated discussion agents with emotion-aware profiles
- A dedicated news curator tool that fetches and deduplicates trending news
- Generated article files stored individually in `data/articles/`
- CLI run modes to generate news articles, run discussion, or both
- Per-agent memory controls (`memory_window_messages` and `include_topic_every_turn`)
- Per-agent generation control (`temperature`)

## Setup

```bash
export OPENAI_API_KEY="your-api-key-here"
export TAVILY_API_KEY="your-tavily-api-key"
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Quick Start

```bash
times-of-agents
```

Default behavior (no mode flags) runs both steps:
1. Generate 3 trending news articles into `data/articles/`
2. Run agent discussion using those articles as topic

## Run Modes

Generate news articles only (saved as individual files):

```bash
times-of-agents --generate-news-topic
```

Run discussion only using existing article files or topic file:

```bash
times-of-agents --agent-discussion
```

Run discussion with inline topic text:

```bash
times-of-agents --agent-discussion --topic "Debate the impact of AI chips on global markets"
```

Run both explicitly:

```bash
times-of-agents --generate-news-topic --agent-discussion
```

Control number of fetched articles:

```bash
times-of-agents --generate-news-topic --news-article-count 5
```

## Generated Files

Articles are stored in `data/articles/` with names like:
- `01_First_article_headline.txt`
- `02_Second_article_headline.txt`
- `03_Third_article_headline.txt`

Each file contains the article title, source, link, and full summary.

## Tools

The Tavily search tool can be used by agents to retrieve web results:

```python
from times_of_agents.infrastructure.tavily_search_tool import tavily_search_tool

payload = tavily_search_tool.run(query="latest AI chip export rules", max_results=3)
```

## Agent Config Memory Controls

Each item in `data/agents.json` can tune context behavior per agent:

- `memory_window_messages`: number of recent transcript messages included in prompts for that agent (for example `5`, `10`, `15`)
- `include_topic_every_turn`:
  - `true` -> include the topic line in every speaking/interjection prompt
  - `false` -> include the topic once for that agent, then rely on conversation context
- `temperature`: controls creativity/randomness per agent (default `0.7`, valid range `0.0` to `2.0`)

Example:

```json
{
  "identity": { "id": "geo-risk-01", "name": "Geo Risk", "role": "Analyst", "description": "..." },
  "emotion_profile": { "trust": 0.6, "anticipation": 0.5, "joy": 0.2, "surprise": 0.3, "fear": 0.6, "sadness": 0.4, "disgust": 0.2, "anger": 0.3 },
  "speaking_weight": 1.1,
  "memory_window_messages": 10,
  "include_topic_every_turn": false,
  "temperature": 0.8
}
```
