"""Publish compact book packages into the direct content catalog."""

from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import uuid

from ..config import RootConfig
from .small import validate_small_package


def import_package(roots: RootConfig, source: str | Path) -> dict[str, str]:
    """Atomically copy one validated compact package into the catalog."""
    package = Path(source).resolve()
    if not package.is_dir() or not (package / "book.json").is_file():
        raise FileNotFoundError("book package must be a directory containing book.json")
    errors = validate_small_package(package)
    if errors:
        raise ValueError("package failed strict validation: " + "; ".join(errors))
    declaration = json.loads((package / "book.json").read_text(encoding="utf-8"))
    from ..catalog import catalog_root, list_books
    target_root = catalog_root(roots)
    target_root.mkdir(parents=True, exist_ok=True)
    target = target_root / package.name
    if target.exists():
        raise FileExistsError(f"book package already exists and is immutable: {target.name}")
    staging = target_root / f".{package.name}.import-{uuid.uuid4().hex}"
    try:
        shutil.copytree(package, staging)
        copied_errors = validate_small_package(staging)
        if copied_errors:
            raise ValueError("copied package failed strict validation: " + "; ".join(copied_errors))
        # The staging directory is visible to the catalog here, so this checks
        # the prospective package against every published stable ID before it
        # becomes permanent.
        list_books(roots)
        os.replace(staging, target)
    except Exception:
        if staging.exists():
            shutil.rmtree(staging)
        raise
    return {"status": "imported", "package": str(target), "book_id": str(declaration["book_id"])}
