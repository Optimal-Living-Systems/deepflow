.PHONY: help install-runtime install-langflow test test-runtime test-components test-integration lint format check serve clean

help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# ─── Installation ─────────────────────────────────────────────

install-runtime: ## Set up the Deep Flo runtime environment
	python3 -m venv .venv-runtime
	. .venv-runtime/bin/activate && pip install -e ".[runtime,dev]"
	@echo ""
	@echo "Runtime environment ready. Activate with:"
	@echo "  source .venv-runtime/bin/activate"

install-langflow: ## Set up the Langflow environment
	python3 -m venv .venv-langflow
	. .venv-langflow/bin/activate && pip install langflow && pip install -e ".[langflow-dev]"
	. .venv-langflow/bin/activate && cp langflow_components/*.py $$(python3 -c "import pathlib; print(pathlib.Path.home() / '.langflow' / 'components')")/
	@echo ""
	@echo "Langflow environment ready. Activate with:"
	@echo "  source .venv-langflow/bin/activate"

# ─── Testing ──────────────────────────────────────────────────

test: ## Run all tests (runtime venv must be active)
	pytest tests/ -v --tb=short

test-runtime: ## Run runtime server tests only
	pytest tests/test_runtime.py -v --tb=short

test-components: ## Run Langflow component tests only
	pytest tests/test_components.py -v --tb=short

test-integration: ## Run end-to-end integration tests (both services must be running)
	pytest tests/test_integration.py -v --tb=short

test-cov: ## Run tests with coverage report
	pytest tests/ -v --tb=short --cov=src/deep_flo_runtime --cov=langflow_components --cov-report=term-missing

# ─── Code Quality ─────────────────────────────────────────────

lint: ## Run ruff linter
	ruff check src/ langflow_components/ tests/

format: ## Auto-format code with ruff
	ruff format src/ langflow_components/ tests/

typecheck: ## Run mypy type checker
	mypy src/deep_flo_runtime/

check: lint typecheck test ## Run all checks (lint + type check + tests)

# ─── Running Services ─────────────────────────────────────────

serve: ## Start the Deep Flo runtime server
	deep-flo-runtime serve --port $${DEEP_FLO_PORT:-8100}

serve-dev: ## Start the runtime in development mode with auto-reload
	uvicorn deep_flo_runtime.server:app --host 0.0.0.0 --port $${DEEP_FLO_PORT:-8100} --reload

docker-up: ## Start both services via Docker Compose
	docker compose -f deploy/docker-compose.yml up

docker-down: ## Stop Docker Compose services
	docker compose -f deploy/docker-compose.yml down

docker-build: ## Build Docker images
	docker compose -f deploy/docker-compose.yml build

# ─── Health Checks ────────────────────────────────────────────

health: ## Check runtime health
	@curl -sf http://localhost:$${DEEP_FLO_PORT:-8100}/health | python3 -m json.tool || echo "Runtime not reachable on port $${DEEP_FLO_PORT:-8100}"

ready: ## Check runtime readiness
	@curl -sf http://localhost:$${DEEP_FLO_PORT:-8100}/ready | python3 -m json.tool || echo "Runtime not ready on port $${DEEP_FLO_PORT:-8100}"

# ─── Cleanup ──────────────────────────────────────────────────

clean: ## Remove virtual environments and build artifacts
	rm -rf .venv-runtime .venv-langflow
	rm -rf build/ dist/ *.egg-info src/*.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
