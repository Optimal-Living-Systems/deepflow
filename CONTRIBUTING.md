# Contributing to Deep Flo

Deep Flo is an [Optimal Living Systems](https://github.com/Optimal-Living-Systems) project — a mutual aid nonprofit building open-source AI infrastructure for community benefit. We welcome contributions from developers of all levels.

---

## Quick Reference

| What | Where |
|------|-------|
| Report a bug | [Open an issue](https://github.com/Optimal-Living-Systems/deep-flo/issues/new) |
| Suggest a feature | [Open an issue](https://github.com/Optimal-Living-Systems/deep-flo/issues/new) |
| Ask a question | [Discussions](https://github.com/Optimal-Living-Systems/deep-flo/discussions) |
| Submit a fix | Fork → branch → PR (see below) |

---

## Development Setup

Deep Flo requires two Python environments due to the LangChain version conflict. See [ARCHITECTURE.md](docs/ARCHITECTURE.md) for why.

### 1. Clone the repository

```bash
git clone https://github.com/Optimal-Living-Systems/deep_flo.git
cd deep-flo
```

### 2. Set up the runtime environment

```bash
python3 -m venv .venv-runtime
source .venv-runtime/bin/activate
pip install -e ".[runtime,dev]"
```

### 3. Set up the Langflow environment (if working on components)

```bash
python3 -m venv .venv-langflow
source .venv-langflow/bin/activate
pip install langflow
pip install -e ".[langflow-dev]"
```

### 4. Run tests

```bash
# Activate the runtime venv
source .venv-runtime/bin/activate

# Run all tests
make test

# Run specific test suites
make test-runtime     # Runtime server tests
make test-components  # Langflow component tests (uses mock runtime)
make test-integration # End-to-end tests (requires both services running)
```

### 5. Linting and formatting

```bash
make lint    # Run ruff linter
make format  # Auto-format with ruff
make check   # Run all checks (lint + type check + tests)
```

---

## Project Structure

```
deep-flo/
├── src/deep_flo_runtime/     # FastAPI server wrapping Deep Agents
│   ├── __init__.py
│   ├── server.py             # FastAPI app and endpoint handlers
│   ├── agent.py              # Deep Agent creation and management
│   └── config.py             # Environment variable handling
├── langflow_components/      # Custom Langflow nodes
│   ├── deep-flo_agent.py     # Main Deep Flo Agent component
│   └── __init__.py
├── deploy/                   # Docker Compose and deployment configs
│   ├── docker-compose.yml
│   ├── Dockerfile.runtime
│   └── Dockerfile.langflow
├── docs/                     # Documentation
│   ├── ARCHITECTURE.md       # Technical design
│   ├── QUICKSTART.md         # Getting started guide
│   └── API-REFERENCE.md      # Runtime API docs
├── examples/langflow/        # Example Langflow flow JSON files
├── skills/                   # Deep Agents skills definitions
├── tests/                    # Test suite
│   ├── test_runtime.py       # Runtime unit tests
│   ├── test_components.py    # Component unit tests
│   └── test_integration.py   # End-to-end tests
├── .github/workflows/        # CI/CD
│   └── ci.yml
├── pyproject.toml            # Package configuration
├── Makefile                  # Development commands
├── README.md
├── CONTRIBUTING.md           # This file
└── LICENSE                   # Apache 2.0
```

---

## Making Changes

### Branch naming

```
feature/short-description    # New features
fix/short-description        # Bug fixes
docs/short-description       # Documentation changes
ci/short-description         # CI/CD changes
```

### Commit messages

Use clear, imperative-mood commit messages:

```
Add streaming support to runtime /stream endpoint
Fix timeout handling in Langflow component
Update architecture docs with Docker deployment diagram
```

### Pull request process

1. Fork the repository
2. Create a feature branch from `main`
3. Make your changes
4. Run `make check` to ensure tests pass and linting is clean
5. Push to your fork
6. Open a PR against `main`
7. Describe what you changed and why in the PR description

### What makes a good PR

- **Focused:** One logical change per PR. Don't mix unrelated fixes.
- **Tested:** Include tests for new functionality. Update tests for changed behavior.
- **Documented:** Update docs if your change affects the user-facing API or architecture.
- **Small:** Smaller PRs get reviewed faster. If your change is large, consider splitting it.

---

## Areas Where Help Is Needed

### Good first issues

- Documentation improvements (typos, clarity, examples)
- Additional example Langflow flows
- Test coverage expansion
- Docker Compose improvements

### Medium complexity

- Streaming response support in the Langflow component
- Additional Deep Agents tool wrappers
- Runtime health check improvements
- Error message improvements

### High complexity

- Runtime connection pooling and agent reuse
- Multi-model configuration in a single flow
- Langflow component for Deep Agents sub-agent management
- Memory/thread persistence across Langflow sessions

Check the [issues page](https://github.com/Optimal-Living-Systems/deep-flo/issues) for current priorities.

---

## Code Style

- **Python:** Follow PEP 8. We use `ruff` for linting and formatting.
- **YAML:** 2-space indentation.
- **Markdown:** One sentence per line in documentation (makes diffs cleaner).
- **Type hints:** Required for all public functions.
- **Docstrings:** Required for all public functions and classes. Use Google style.

---

## License

By contributing to Deep Flo, you agree that your contributions will be licensed under the [Apache 2.0 License](LICENSE).

---

## Code of Conduct

We follow the [Contributor Covenant](https://www.contributor-covenant.org/version/2/1/code_of_conduct/) code of conduct. Be kind, be respectful, be constructive.

---

## Questions?

Open a [discussion](https://github.com/Optimal-Living-Systems/deep-flo/discussions) or reach out to the Optimal Living Systems team. We're happy to help contributors get oriented.
