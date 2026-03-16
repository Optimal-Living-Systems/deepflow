#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "${SCRIPT_DIR}/.." && pwd)"
LANGFLOW_ROOT="${LANGFLOW_ROOT:-${REPO_ROOT}/../langflow}"

export LANGFLOW_COMPONENTS_PATH="${REPO_ROOT}/langflow_components"
export DEEP_FLO_RUNTIME_URL="${DEEP_FLO_RUNTIME_URL:-http://127.0.0.1:8011}"
POSTGRES_PORT="${LANGFLOW_POSTGRES_PORT:-55433}"
export LANGFLOW_DATABASE_URL="${LANGFLOW_DATABASE_URL:-postgresql://langflow:langflow@127.0.0.1:${POSTGRES_PORT}/langflow}"

cd "${LANGFLOW_ROOT}"
exec make run_cli open_browser=false
