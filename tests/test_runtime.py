"""Runtime server unit tests."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from deepflow_runtime.config import DeepFlowSettings
from deepflow_runtime.runtime_api import create_app, extract_text
from langchain_core.messages import AIMessage


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def client() -> TestClient:
    """Test client with no API key (open access, no model configured)."""
    return TestClient(create_app(), raise_server_exceptions=False)


@pytest.fixture
def client_with_key() -> TestClient:
    """Test client with API key authentication enabled."""
    return TestClient(create_app(DeepFlowSettings(api_key="test-secret")), raise_server_exceptions=False)


# ---------------------------------------------------------------------------
# extract_text unit tests (no I/O)
# ---------------------------------------------------------------------------

def test_extract_text_returns_last_ai_message() -> None:
    messages = [AIMessage(content="first"), AIMessage(content="second")]
    assert extract_text(messages) == "second"


def test_extract_text_empty() -> None:
    assert extract_text([]) == ""


def test_extract_text_list_content() -> None:
    messages = [AIMessage(content=[{"type": "text", "text": "hello"}, {"type": "text", "text": "world"}])]
    assert extract_text(messages) == "hello\nworld"


# ---------------------------------------------------------------------------
# GET /health
# ---------------------------------------------------------------------------

def test_health_endpoint(client: TestClient) -> None:
    """Health endpoint returns 200 with status healthy."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_health_public_when_api_key_set(client_with_key: TestClient) -> None:
    """Health endpoint must not require auth."""
    response = client_with_key.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


# ---------------------------------------------------------------------------
# GET /ready
# ---------------------------------------------------------------------------

def test_ready_endpoint(client: TestClient) -> None:
    """Ready endpoint returns 200 or 503 — never 404."""
    response = client.get("/ready")
    assert response.status_code in (200, 503)


# ---------------------------------------------------------------------------
# POST /run — validation and auth
# ---------------------------------------------------------------------------

def test_run_missing_message(client: TestClient) -> None:
    """Run endpoint validates the required message field."""
    response = client.post("/run", json={})
    assert response.status_code in (400, 422)


def test_run_empty_prompt(client: TestClient) -> None:
    """Run endpoint rejects empty prompt."""
    response = client.post("/run", json={"prompt": ""})
    assert response.status_code == 422


def test_run_reaches_model_layer(client: TestClient) -> None:
    """Valid run request passes validation and reaches model layer (503, not 404/422)."""
    response = client.post("/run", json={"prompt": "test", "thread_id": "t1"})
    assert response.status_code not in (404, 422)


def test_run_rejects_missing_token(client_with_key: TestClient) -> None:
    """With API key configured, /run returns 401 for missing token."""
    response = client_with_key.post("/run", json={"prompt": "hello"})
    assert response.status_code == 401


def test_run_rejects_wrong_token(client_with_key: TestClient) -> None:
    """With API key configured, /run returns 401 for wrong token."""
    response = client_with_key.post(
        "/run",
        json={"prompt": "hello"},
        headers={"Authorization": "Bearer wrong"},
    )
    assert response.status_code == 401


def test_run_accepts_correct_token(client_with_key: TestClient) -> None:
    """Correct Bearer token passes auth."""
    response = client_with_key.post(
        "/run",
        json={"prompt": "hello"},
        headers={"Authorization": "Bearer test-secret"},
    )
    # 503 = past auth, no model configured — correct
    assert response.status_code == 503


# ---------------------------------------------------------------------------
# POST /invoke — backwards-compatible alias
# ---------------------------------------------------------------------------

def test_invoke_still_works(client: TestClient) -> None:
    """/invoke endpoint still works alongside /run."""
    response = client.post("/invoke", json={"prompt": "hello"})
    assert response.status_code not in (404, 422)


# ---------------------------------------------------------------------------
# POST /stream — auth mirrors /run
# ---------------------------------------------------------------------------

def test_stream_rejects_wrong_token(client_with_key: TestClient) -> None:
    response = client_with_key.post(
        "/stream",
        json={"prompt": "hello"},
        headers={"Authorization": "Bearer bad"},
    )
    assert response.status_code == 401
