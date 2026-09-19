"""Root configuration and safe path resolution.

The configuration is deliberately small.  Feature-specific policy stays in the
skill that owns it; this module only resolves the system/data boundary.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any


class ConfigError(ValueError):
    """Raised when an existing configuration is malformed or unsafe."""


@dataclass(frozen=True)
class RootConfig:
    system_root: Path
    data_root: Path

    def data_path(self, *parts: str) -> Path:
        candidate = self.data_root.joinpath(*parts)
        _ensure_within(candidate, self.data_root)
        return candidate

    def system_path(self, *parts: str) -> Path:
        candidate = self.system_root.joinpath(*parts)
        _ensure_within(candidate, self.system_root)
        return candidate


def _ensure_within(candidate: Path, root: Path) -> None:
    """Reject traversal while allowing paths that do not exist yet."""
    root_abs = root.resolve()
    candidate_abs = candidate.resolve(strict=False)
    try:
        candidate_abs.relative_to(root_abs)
    except ValueError as exc:
        raise ConfigError(f"path escapes declared root: {candidate_abs}") from exc


def _path(value: Any, field: str, base: Path) -> Path:
    if isinstance(value, Path):
        return value.expanduser().resolve(strict=False)
    if not isinstance(value, str) or not value.strip():
        raise ConfigError(f"{field} must be a non-empty path")
    p = Path(value).expanduser()
    return (p if p.is_absolute() else base / p).resolve(strict=False)


def resolve_roots(
    project_root: str | Path | None = None,
    *,
    config_path: str | Path | None = None,
    system_root: str | Path | None = None,
    data_root: str | Path | None = None,
) -> RootConfig:
    """Resolve the system and data roots."""
    project = Path(project_root or Path.cwd()).resolve()
    cfg_path = Path(config_path) if config_path else project / ".booksys" / "config.json"
    raw: dict[str, Any] = {}
    if cfg_path.exists():
        try:
            loaded = json.loads(cfg_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            raise ConfigError(f"cannot parse configuration {cfg_path}: {exc}") from exc
        if not isinstance(loaded, dict):
            raise ConfigError("root configuration must be a JSON object")
        raw = loaded

    resolved_system = _path(system_root if system_root is not None else raw.get("system_root", project), "system_root", project)
    configured_data = data_root if data_root is not None else raw.get("data_root")
    resolved_data = _path(configured_data if configured_data is not None else project, "data_root", project)

    if not resolved_system.exists() or not resolved_system.is_dir():
        raise ConfigError(f"system_root must be an existing directory: {resolved_system}")
    return RootConfig(resolved_system, resolved_data)
