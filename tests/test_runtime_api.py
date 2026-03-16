from __future__ import annotations

import httpx
import pytest
from langchain_core.messages import AIMessage

from deepflow_runtime.config import DeepFlowSettings
from deepflow_runtime.runtime_api import create_app, extract_text


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _app(api_key: str | None = None):
    return create_app(DeepFlowSettings(api_key=api_key))


# ---------------------------------------------------------------------------
# extract_text
# ---------------------------------------------------------------------------

def test_extract_text_returns_latest_ai_message():
    messages = [
        AIMessage(content="first"),
        AIMessage(content=[{"type": "text", "text": "second"}]),
    ]
    assert extract_text(messages) == "second"


def test_extract_text_empty_list():
    assert extract_text([]) == ""


def test_extract_text_list_content_joined():
    messages = [AIMessage(content=[{"type": "text", "text": "hello"}, {"type": "text", "text": "world"}])]
    assert extract_text(messages) == "hello\nworld"


# ---------------------------------------------------------------------------
# /health — always public
# ---------------------------------------------------------------------------

@pytest.mark.anyio
async def test_health_returns_ok():
    transport = httpx.ASGITransport(app=create_app())
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert "provider_status" in response.json()


@pytest.mark.anyio
async def test_health_public_when_api_key_set():
    """Monitoring tools must be able to reach /health without credentials."""
    transport = httpx.ASGITransport(app=_app(api_key="secret"))
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.get("/health")
    assert response.status_code == 200


# ---------------------------------------------------------------------------
# /invoke — model errors
# ---------------------------------------------------------------------------

@pytest.mark.anyio
async def test_invoke_returns_503_without_model_credentials():
    transport = httpx.ASGITransport(app=create_app())
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.post("/invoke", json={"prompt": "hello", "thread_id": "t1"})
    assert response.status_code == 503


# ---------------------------------------------------------------------------
# /invoke — auth
# ---------------------------------------------------------------------------

@pytest.mark.anyio
async def test_invoke_open_when_api_key_unset():
    """No DEEPFLOW_API_KEY → /invoke is open, reaches the model layer."""
    transport = httpx.ASGITransport(app=_app(api_key=None))
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.post("/invoke", json={"prompt": "hello"})
    assert response.status_code == 503  # past auth, fails on missing model


@pytest.mark.anyio
async def test_invoke_rejects_missing_token():
    transport = httpx.ASGITransport(app=_app(api_key="secret"))
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.post("/invoke", json={"prompt": "hello"})
    assert response.status_code == 401


@pytest.mark.anyio
async def test_invoke_rejects_wrong_token():
    transport = httpx.ASGITransport(app=_app(api_key="secret"))
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.post(
            "/invoke",
            json={"prompt": "hello"},
            headers={"Authorization": "Bearer wrong"},
        )
    assert response.status_code == 401


@pytest.mark.anyio
async def test_invoke_accepts_correct_token():
    transport = httpx.ASGITransport(app=_app(api_key="secret"))
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.post(
            "/invoke",
            json={"prompt": "hello"},
            headers={"Authorization": "Bearer secret"},
        )
    assert response.status_code == 503  # past auth, fails on missing model


# ---------------------------------------------------------------------------
# /invoke/stream — auth mirrors /invoke
# ---------------------------------------------------------------------------

@pytest.mark.anyio
async def test_stream_rejects_missing_token():
    transport = httpx.ASGITransport(app=_app(api_key="secret"))
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.post("/invoke/stream", json={"prompt": "hello"})
    assert response.status_code == 401


@pytest.mark.anyio
async def test_stream_rejects_wrong_token():
    transport = httpx.ASGITransport(app=_app(api_key="secret"))
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.post(
            "/invoke/stream",
            json={"prompt": "hello"},
            headers={"Authorization": "Bearer bad"},
        )
    assert response.status_code == 401


# ---------------------------------------------------------------------------
# Request validation
# ---------------------------------------------------------------------------

@pytest.mark.anyio
async def test_invoke_rejects_empty_prompt():
    transport = httpx.ASGITransport(app=create_app())
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.post("/invoke", json={"prompt": ""})
    assert response.status_code == 422


@pytest.mark.anyio
async def test_invoke_default_thread_id_accepted():
    """Omitting thread_id should not cause a 422."""
    transport = httpx.ASGITransport(app=create_app())
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.post("/invoke", json={"prompt": "hello"})
    assert response.status_code != 422
