"""Validation for the compact book package consumed by all four skills."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any
from urllib.parse import unquote

from ..domain.contracts import ContractError, validate_identifier


SMALL_PACKAGE_VERSION = 1
CHAPTER_RESOURCES = ("source.md", "guide.md", "concepts.json")

# The target of a markdown link or image: the first token after ``](``.
_MARKDOWN_TARGET = re.compile(r"\]\(\s*([^)\s]+)")
# An absolute URI scheme such as ``https:``, ``mailto:``, or ``tel:``.
_URI_SCHEME = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.\-]*:")


def validate_small_package(package_root: str | Path) -> list[str]:
    """Return actionable diagnostics for a compact book package."""
    root = Path(package_root).resolve()
    errors: list[str] = []
    declaration_path = root / "book.json"
    if not root.is_dir():
        return [f"package root missing: {root}"]
    if not declaration_path.is_file():
        return ["book.json is required"]
    try:
        declaration = json.loads(declaration_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return [f"cannot parse book.json: {exc}"]
    if not isinstance(declaration, dict):
        return ["book.json must be an object"]
    if declaration.get("schema_version") != SMALL_PACKAGE_VERSION:
        errors.append(f"schema_version must be {SMALL_PACKAGE_VERSION}")
    try:
        validate_identifier(declaration.get("book_id"), "book_id")
    except ContractError as exc:
        errors.append(str(exc))
    if not isinstance(declaration.get("title"), str) or not declaration["title"].strip():
        errors.append("title must be a non-empty string")
    if not (root / "book.md").is_file() or not (root / "book.md").read_text(encoding="utf-8").strip():
        errors.append("book.md must be a non-empty file")
    chapters = declaration.get("chapters")
    if not isinstance(chapters, list) or not chapters:
        errors.append("chapters must be a non-empty list")
        return errors
    seen_chapters: set[str] = set()
    seen_concepts: set[str] = set()
    for index, chapter in enumerate(chapters):
        if not isinstance(chapter, dict):
            errors.append(f"chapters[{index}] must be an object")
            continue
        chapter_id = chapter.get("chapter_id")
        slug = chapter.get("slug")
        try:
            validate_identifier(chapter_id, f"chapters[{index}].chapter_id")
        except ContractError as exc:
            errors.append(str(exc))
        if chapter_id in seen_chapters:
            errors.append(f"duplicate chapter id: {chapter_id}")
        seen_chapters.add(chapter_id)
        if not isinstance(slug, str) or not slug.strip() or Path(slug).name != slug:
            errors.append(f"chapters[{index}].slug must be a safe directory name")
            continue
        chapter_root = (root / "chapters" / slug).resolve(strict=False)
        try:
            chapter_root.relative_to((root / "chapters").resolve())
        except ValueError:
            errors.append(f"chapter path escapes package root: {slug}")
            continue
        if not chapter_root.is_dir():
            errors.append(f"chapter directory missing: {slug}")
            continue
        for resource in CHAPTER_RESOURCES:
            path = chapter_root / resource
            if not path.is_file() or (resource != "concepts.json" and not path.read_text(encoding="utf-8").strip()):
                errors.append(f"chapter {slug} missing or empty resource: {resource}")
        concepts_path = chapter_root / "concepts.json"
        if not concepts_path.is_file():
            continue
        try:
            concepts_payload: Any = json.loads(concepts_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            errors.append(f"chapter {slug} concepts.json invalid: {exc}")
            continue
        concepts = concepts_payload
        if not isinstance(concepts, list):
            errors.append(f"chapter {slug} concepts must be a list")
            continue
        for concept_index, concept in enumerate(concepts):
            if not isinstance(concept, dict):
                errors.append(f"chapter {slug} concepts[{concept_index}] must be an object")
                continue
            concept_id = concept.get("id")
            try:
                validate_identifier(concept_id, f"chapter {slug} concepts[{concept_index}].id")
            except ContractError as exc:
                errors.append(str(exc))
            if concept_id in seen_concepts:
                errors.append(f"duplicate concept id: {concept_id}")
            seen_concepts.add(concept_id)
            if not isinstance(concept.get("name"), str) or not concept["name"].strip():
                errors.append(f"chapter {slug} concepts[{concept_index}].name must be non-empty")
    return errors


def validate_book_md_links(package_root: str | Path, system_root: str | Path) -> list[str]:
    """Return diagnostics for relative ``book.md`` links that do not resolve.

    Link targets are written relative to the book-system root (the directory the
    ``_book_system_root.txt`` anchor points at), so a target is accepted when it
    resolves to an existing entry beneath either the system root or the package
    root. Absolute URIs, bare anchors, and fragments are ignored.
    """
    package = Path(package_root).resolve()
    book_md = package / "book.md"
    if not book_md.is_file():
        return []
    try:
        text = book_md.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        return [f"cannot read book.md: {exc}"]
    system = Path(system_root).resolve()
    errors: list[str] = []
    seen: set[str] = set()
    for match in _MARKDOWN_TARGET.finditer(text):
        target = _local_link_target(match.group(1))
        if target is None or target in seen:
            continue
        seen.add(target)
        if _existing_under(system, target) is None and _existing_under(package, target) is None:
            errors.append(f"book.md link target missing: {target}")
    return errors


def _local_link_target(raw: str) -> str | None:
    """Return the local path of a link target, or ``None`` for external links."""
    target = raw.strip().strip("<>")
    if not target or target.startswith("#") or target.startswith("//"):
        return None
    if _URI_SCHEME.match(target):
        return None
    target = target.split("#", 1)[0].split("?", 1)[0].strip()
    return unquote(target) or None


def _existing_under(base: Path, target: str) -> Path | None:
    """Resolve ``target`` under ``base``, returning it only if it exists inside."""
    try:
        candidate = (base / target).resolve(strict=False)
        candidate.relative_to(base)
    except (OSError, ValueError):
        return None
    return candidate if candidate.exists() else None
