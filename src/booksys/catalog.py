"""Direct catalog lookup for compact book packages.

The catalog answers only two questions: which packages are declared, and where
the declared resources of a given stable identity live. It performs no semantic
matching, ranking, or disambiguation, and never returns candidates for the
caller to choose from -- resolving a name or alias to a stable identity belongs
to the caller, which reads the declaration itself.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .config import RootConfig
from .packages.small import validate_small_package


class CatalogError(ValueError):
    pass


def catalog_root(roots: RootConfig) -> Path:
    return roots.system_path(".booksys", "content", "books")


def read_declaration(package_path: str | Path) -> dict[str, Any]:
    """Return the verbatim ``book.json`` declaration of a validated package."""
    package = Path(package_path)
    errors = validate_small_package(package)
    if errors:
        raise CatalogError(f"invalid book package {package.name}: " + "; ".join(errors))
    return json.loads((package / "book.json").read_text(encoding="utf-8"))


def list_books(roots: RootConfig) -> list[dict[str, Any]]:
    """Return the declared identity, location, and chapter map of every package.

    All stable identities are global to a catalog.  Detecting a collision here
    keeps every caller from silently selecting the first matching package.
    """
    root = catalog_root(roots)
    if not root.is_dir():
        raise CatalogError(f"book catalog is missing: {root}")
    books: list[dict[str, Any]] = []
    seen: dict[str, str] = {}

    def claim(identifier: str, location: Path) -> None:
        prior = seen.get(identifier)
        if prior:
            raise CatalogError(f"duplicate stable id {identifier}: {prior}; {location}")
        seen[identifier] = str(location)

    for package in sorted(p for p in root.iterdir() if p.is_dir() and (p / "book.json").is_file()):
        declaration = read_declaration(package)
        claim(declaration["book_id"], package / "book.json")
        for chapter in declaration["chapters"]:
            chapter_root = package / "chapters" / chapter["slug"]
            claim(chapter["chapter_id"], chapter_root)
            concepts = json.loads((chapter_root / "concepts.json").read_text(encoding="utf-8"))
            for concept in concepts:
                claim(concept["id"], chapter_root / "concepts.json")
        books.append({
            "book_id": declaration["book_id"],
            "package_path": str(package),
            "chapters": [{"chapter_id": chapter["chapter_id"], "slug": chapter["slug"]} for chapter in declaration["chapters"]],
        })
    return books


def select_book(roots: RootConfig, book_id: str) -> dict[str, Any]:
    """Return one declared book by its stable identifier."""
    for book in list_books(roots):
        if book["book_id"] == book_id:
            return book
    raise CatalogError(f"unknown book id: {book_id}")


def locate_chapter(roots: RootConfig, book_id: str, chapter_id: str) -> dict[str, Any]:
    """Return the declared resource paths of one chapter by stable identifiers."""
    book = select_book(roots, book_id)
    slug = next((chapter["slug"] for chapter in book["chapters"] if chapter["chapter_id"] == chapter_id), None)
    if slug is None:
        raise CatalogError(f"unknown chapter id: {chapter_id}")
    chapter_root = Path(book["package_path"]) / "chapters" / slug
    return {
        "book_id": book["book_id"],
        "chapter_id": chapter_id,
        "slug": slug,
        "chapter_path": str(chapter_root),
        "source_path": str(chapter_root / "source.md"),
        "guide_path": str(chapter_root / "guide.md"),
        "concepts_path": str(chapter_root / "concepts.json"),
    }


def locate_concept(roots: RootConfig, concept_id: str) -> dict[str, Any]:
    """Return the owning chapter resource paths of one concept by its stable identifier."""
    for book in list_books(roots):
        for chapter in book["chapters"]:
            concepts_path = Path(book["package_path"]) / "chapters" / chapter["slug"] / "concepts.json"
            for concept in json.loads(concepts_path.read_text(encoding="utf-8")):
                if concept.get("id") == concept_id:
                    return {
                        "book_id": book["book_id"],
                        "chapter_id": chapter["chapter_id"],
                        "slug": chapter["slug"],
                        "concepts_path": str(concepts_path),
                    }
    raise CatalogError(f"unknown concept id: {concept_id}")
