# Deployment

Deep Flo now ships two deployment entry points.

## 1. PostgreSQL for local source Langflow

Use this when you want to keep running Langflow from the local checkout but move its database off SQLite.

Start Postgres:

```bash
./scripts/start_postgres.sh
```

Stop Postgres:

```bash
./scripts/stop_postgres.sh
```

Start local Langflow against that database:

```bash
./scripts/start_langflow_postgres.sh
```

Default local database URL:

```env
LANGFLOW_DATABASE_URL=postgresql://langflow:langflow@127.0.0.1:55433/langflow
```

Override the published host port if needed:

```bash
export LANGFLOW_POSTGRES_PORT=55433
```

If the local Langflow source environment cannot load `libpq`, install:

```bash
cd /path/to/langflow
uv pip install 'psycopg[binary]'
```

## 2. Full container stack

Use this when you want a single Docker Compose stack for:

- PostgreSQL
- Deep Flo runtime API
- Deep Flo MCP server
- Langflow

Start it:

```bash
./scripts/start_compose_stack.sh
```

Stop it:

```bash
./scripts/stop_compose_stack.sh
```

Compose file:
- [docker-compose.stack.yml](docker-compose.stack.yml)

This stack expects:
- model provider keys in the repo `.env`
- Docker access on the host

Important:
- `docker compose config` will inline values from `.env`, so treat that output as sensitive
