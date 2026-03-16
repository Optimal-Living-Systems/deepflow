"""CLI banner support for Deep Flo."""

from __future__ import annotations

from pathlib import Path


def print_banner() -> None:
    """Print the shared Deep Flo ASCII banner."""
    banner_path = Path(__file__).resolve().parents[3] / "assets" / "ascii" / "deep_flo_banner.txt"
    print(banner_path.read_text(encoding="utf-8"))
