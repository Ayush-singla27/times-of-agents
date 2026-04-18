# AgentPress Backend (CLI)

An agentic Python backend for a multi-agent news discussion system powered by **CrewAI** and GPT-4o mini (OpenAI).

## What This Base Includes

- **CrewAI-orchestrated agents** — each agent is a `crewai.Agent` with a role, goal, and Plutchik-emotion backstory
- **Sequential per-round Crew execution** — one `Crew` per discussion round keeps context windows small and ordering reproducible
- Configurable AI agent profiles with Plutchik emotion parameters (`data/agents.json`)
- Topic loading from a local file (`data/topic.txt`)
- Weight-randomised agent ordering (seeded for reproducibility)
- Clean layered architecture: domain → application → infrastructure → interfaces

## Setup

```bash
# Set OpenAI API key
export OPENAI_API_KEY="your-api-key-here"

# Optional: token pricing for cost estimation (GPT-4o mini)
export TOKEN_INPUT_COST_PER_1K_USD=0.00015
export TOKEN_OUTPUT_COST_PER_1K_USD=0.00060

# Create environment and install
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Quick Start

```bash
times-of-agents --rounds 2
```

## Local Files You Can Edit

- Topic: `data/topic.txt`
- Agents and emotion parameters: `data/agents.json`


## Emotion Parameters

Each agent supports a Plutchik-inspired profile baked into its `backstory`:

| Key           | Range     |
|---------------|-----------|
| `trust`       | 0.0 – 1.0 |
| `anticipation`| 0.0 – 1.0 |
| `joy`         | 0.0 – 1.0 |
| `surprise`    | 0.0 – 1.0 |
| `fear`        | 0.0 – 1.0 |
| `sadness`     | 0.0 – 1.0 |
| `disgust`     | 0.0 – 1.0 |
| `anger`       | 0.0 – 1.0 |
