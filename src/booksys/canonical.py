"""Canonical, byte-stable JSON and JSONL serialization."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterator


def dumps(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def iter_jsonl(path: str | Path) -> Iterator[Any]:
    p = Path(path)
    with p.open("r", encoding="utf-8", newline="") as fh:
        for line_no, line in enumerate(fh, 1):
            if not line.strip():
                continue
            try:
                yield json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"invalid JSONL at {p}:{line_no}: {exc.msg}") from exc
