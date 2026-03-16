#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "${SCRIPT_DIR}/.." && pwd)"

cd "${REPO_ROOT}"
exec uv run deep-flo mcp --transport streamable-http --host "${DEEP_FLO_MCP_HOST:-127.0.0.1}" --port "${DEEP_FLO_MCP_PORT:-8012}"
