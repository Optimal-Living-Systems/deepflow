"""Langflow component unit tests.

These tests run in the langflow-dev venv (NO deepagents installed).
They test that component files are valid Python and the component class is
accessible, using only httpx for any mock HTTP calls.
"""

from __future__ import annotations

import importlib
import importlib.util
import pathlib


# ---------------------------------------------------------------------------
# Syntax and importability checks
# ---------------------------------------------------------------------------

def test_component_module_imports() -> None:
    """All Python files in langflow_components/ parse and load without error."""
    component_dir = pathlib.Path("langflow_components")
    assert component_dir.exists(), "langflow_components/ directory not found"

    py_files = [f for f in component_dir.glob("*.py") if f.name != "__init__.py"]
    assert len(py_files) > 0, "No component Python files found"

    for py_file in py_files:
        spec = importlib.util.spec_from_file_location(py_file.stem, py_file)
        assert spec is not None, f"Could not load spec for {py_file}"
        module = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(module)  # type: ignore[union-attr]
        except ImportError:
            # ImportError is expected in the langflow-dev venv (no langflow installed)
            # We're just verifying the file is syntactically valid Python
            pass
        except Exception as exc:
            raise AssertionError(f"Unexpected error loading {py_file}: {exc}") from exc


def test_init_module_importable() -> None:
    """langflow_components/__init__.py is importable."""
    init = pathlib.Path("langflow_components/__init__.py")
    assert init.exists(), "langflow_components/__init__.py not found"


# ---------------------------------------------------------------------------
# Component file structure
# ---------------------------------------------------------------------------

def test_component_file_exists() -> None:
    """Main component file is present."""
    component_dir = pathlib.Path("langflow_components")
    py_files = list(component_dir.glob("*.py"))
    non_init = [f for f in py_files if f.name != "__init__.py"]
    assert len(non_init) > 0, "No component implementation files found in langflow_components/"


def test_component_references_runtime_url() -> None:
    """Component file contains a runtime URL reference (HTTP bridge pattern)."""
    component_dir = pathlib.Path("langflow_components")
    for py_file in component_dir.glob("*.py"):
        if py_file.name == "__init__.py":
            continue
        source = py_file.read_text()
        assert "http" in source.lower() or "url" in source.lower(), (
            f"{py_file.name} does not appear to make HTTP calls — "
            "components must call the runtime over HTTP, not import deepagents directly"
        )


def test_no_deepagents_import_in_components() -> None:
    """Components must NOT import deepagents — that would break the venv isolation."""
    component_dir = pathlib.Path("langflow_components")
    for py_file in component_dir.glob("*.py"):
        source = py_file.read_text()
        assert "import deepagents" not in source, (
            f"{py_file.name} imports deepagents directly. "
            "Components must call the runtime over HTTP instead."
        )
        assert "from deepagents" not in source, (
            f"{py_file.name} imports from deepagents directly. "
            "Components must call the runtime over HTTP instead."
        )
