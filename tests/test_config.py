from deep_flo_runtime.config import DeepFloSettings


def test_settings_paths_use_home_dir(tmp_path):
    settings = DeepFloSettings(home_dir=tmp_path)

    assert settings.workspace_dir == tmp_path / "workspace"
    assert settings.data_dir == tmp_path / "data"
    assert settings.memory_file == tmp_path / "memories" / "AGENTS.md"


def test_provider_status_reports_missing_keys(monkeypatch):
    for key in (
        "ANTHROPIC_API_KEY",
        "OPENAI_API_KEY",
        "GOOGLE_API_KEY",
        "OPENROUTER_API_KEY",
        "DEEPSEEK_API_KEY",
        "TAVILY_API_KEY",
        "LANGSMITH_API_KEY",
    ):
        monkeypatch.delenv(key, raising=False)

    settings = DeepFloSettings()
    assert settings.provider_status() == {
        "anthropic": False,
        "openai": False,
        "google": False,
        "openrouter": False,
        "deepseek": False,
        "tavily": False,
        "langsmith": False,
    }
