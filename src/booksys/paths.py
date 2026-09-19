from __future__ import annotations

from pathlib import Path

from .config import RootConfig


def runtime_root(roots: RootConfig) -> Path:
    """Return the private writable runtime directory."""
    return roots.data_path(".booksys", "runtime")
