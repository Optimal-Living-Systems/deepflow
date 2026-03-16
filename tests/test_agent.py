from deep_flo_runtime.agent import _build_model_from_name


def test_build_openrouter_model(monkeypatch):
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-openrouter-key")
    model = _build_model_from_name("openrouter:anthropic/claude-sonnet-4.5")
    assert type(model).__name__ == "ChatOpenRouter"


def test_build_deepseek_model(monkeypatch):
    monkeypatch.setenv("DEEPSEEK_API_KEY", "test-deepseek-key")
    model = _build_model_from_name("deepseek:deepseek-chat")
    assert type(model).__name__ == "ChatDeepSeek"
