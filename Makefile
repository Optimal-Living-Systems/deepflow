.PHONY: install dev demo serve test doctor

install:
	uv sync

dev:
	uv sync --extra dev

demo: install
	@if [ ! -f .env ]; then \
		echo "No .env file found. Copying .env.example..."; \
		cp .env.example .env; \
		echo "Edit .env and add at least one provider API key, then re-run 'make demo'."; \
		exit 1; \
	fi
	@echo "Running DeepFlow doctor..."
	uv run deepflow doctor
	@echo ""
	@echo "Starting DeepFlow runtime at http://127.0.0.1:8011"
	@echo "  POST /invoke        — blocking response"
	@echo "  POST /invoke/stream — SSE streaming"
	@echo "  GET  /health        — provider status"
	@echo ""
	uv run deepflow serve

serve:
	uv run deepflow serve

test:
	uv run pytest -v

doctor:
	uv run deepflow doctor
