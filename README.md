# Times of Agents API Backend

A production-style Python backend for daily multi-agent news generation and discussion.

## Architecture

- `interfaces/api`: FastAPI app and HTTP routes
- `application`: orchestration and use cases
  - `application/pipelines`: end-to-end flows such as daily topic + discussion generation
  - `application/scheduling`: background job scheduling
  - `application/tools`: external-data tools used by application flows
- `infrastructure`: SQLite store, settings, config readers
- `domain`: core entities and value objects

The system runs one daily generation job, persists results in SQLite, and serves data to frontend clients via HTTP.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Configure Backend

Set API keys in your shell (env vars only):

```bash
export OPENAI_API_KEY="your-openai-key"
export TAVILY_API_KEY="your-tavily-key"
```

All other runtime configuration is read from `data/backend_config.json`.

Update these keys before running:
- `db_path`
- `agents_config_file`
- `articles_dir`
- `model`
- `article_count`
- `rounds`
- `seed`
- `run_on_startup`
- `enable_scheduler`
- `schedule_hour_utc`
- `write_articles_to_files`
- `discussions_per_run`
- `token_input_cost_per_1k_usd`
- `token_output_cost_per_1k_usd`

## Run API Server

```bash
times-of-agents-api
```

- Base URL: `http://localhost:8000`
- Docs: `http://localhost:8000/docs`

## API Endpoints

- `GET /health`
- `GET /api/v1/snapshots/latest`
- `GET /api/v1/snapshots/{run_date}`
- `GET /api/v1/topics/{topic_id}`
- `GET /api/v1/topics/{topic_id}/discussion`
- `POST /api/v1/admin/run-daily-job?force=false&run_date=YYYY-MM-DD`

## Frontend Data Flow

1. Fetch current day data with `GET /api/v1/snapshots/latest`
2. Fetch selected topic details with `GET /api/v1/topics/{topic_id}`
3. Fetch transcript with `GET /api/v1/topics/{topic_id}/discussion`
