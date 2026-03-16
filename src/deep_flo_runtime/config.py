"""Configuration for Deep Flo."""

from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path

from dotenv import dotenv_values
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PROJECT_ENV_PATH = PROJECT_ROOT / ".env"
HOME_ENV_PATH = Path.home() / ".env"


class DeepFloSettings(BaseSettings):
    """Runtime settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_prefix="DEEP_FLO_",
        env_file=(str(PROJECT_ENV_PATH), str(HOME_ENV_PATH)),
        extra="ignore",
    )

    home_dir: Path = Field(default=PROJECT_ROOT)
    host: str = "127.0.0.1"
    port: int = 8011
    api_key: str | None = None
    model: str | None = None
    anthropic_default_model: str = "anthropic:claude-sonnet-4-6"
    openai_default_model: str = "openai:gpt-4.1"
    google_default_model: str = "google_genai:gemini-2.5-pro"
    openrouter_default_model: str = "openrouter:anthropic/claude-sonnet-4.5"
    deepseek_default_model: str = "deepseek:deepseek-chat"
    ollama_default_model: str = "ollama:qwen3:latest"
    request_timeout_seconds: float = 60.0
    user_agent: str = "Deep Flo/0.1 (+https://github.com/langchain-ai/deepagents)"

    @property
    def workspace_dir(self) -> Path:
        return self.home_dir / "workspace"

    @property
    def data_dir(self) -> Path:
        return self.home_dir / "data"

    @property
    def memories_dir(self) -> Path:
        return self.home_dir / "memories"

    @property
    def skills_dir(self) -> Path:
        return self.home_dir / "skills"

    @property
    def memory_file(self) -> Path:
        return self.memories_dir / "AGENTS.md"

    @property
    def sqlite_path(self) -> Path:
        return self.data_dir / "threads.sqlite"

    def ensure_directories(self) -> None:
        """Create the runtime directories if they do not exist."""
        for path in (
            self.home_dir,
            self.workspace_dir,
            self.data_dir,
            self.memories_dir,
            self.skills_dir,
        ):
            path.mkdir(parents=True, exist_ok=True)

    def provider_status(self) -> dict[str, bool]:
        """Return provider availability without exposing secret values."""
        return {
            "anthropic": bool(os.getenv("ANTHROPIC_API_KEY")),
            "openai": bool(os.getenv("OPENAI_API_KEY")),
            "google": bool(os.getenv("GOOGLE_API_KEY")),
            "openrouter": bool(os.getenv("OPENROUTER_API_KEY")),
            "deepseek": bool(os.getenv("DEEPSEEK_API_KEY")),
            "tavily": bool(os.getenv("TAVILY_API_KEY")),
            "langsmith": bool(os.getenv("LANGSMITH_API_KEY")),
        }


@lru_cache(maxsize=1)
def get_settings() -> DeepFloSettings:
    """Return cached Deep Flo settings."""
    for key, value in dotenv_values(PROJECT_ENV_PATH).items():
        if value is not None:
            os.environ.setdefault(key, value)
    for key, value in dotenv_values(HOME_ENV_PATH).items():
        if value is not None:
            os.environ.setdefault(key, value)
    settings = DeepFloSettings()
    settings.ensure_directories()
    return settings
