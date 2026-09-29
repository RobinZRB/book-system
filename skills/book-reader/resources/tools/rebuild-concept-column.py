#!/usr/bin/env python3
"""Rebuild a package's ``book.md`` chapter-index concept column.

The concept column is a projection of each chapter's ``concepts.json``. Concept
names and stable IDs have exactly one home, the ``concepts.json`` file; the
column in ``book.md`` only mirrors the names, so that a reader — human or model —
has a chapter overview without opening twenty files. It must therefore list every
concept of a chapter, in the order that file declares them.

Nothing else validates that column. Package validation checks that ``book.md`` is
non-empty and that the links in its reference column resolve, and stops there, so
a hand-written or stale column fails silently: a concept added to
``concepts.json`` and missed here becomes invisible at chapter-selection time.
Run this after every change to a chapter's ``concepts.json``.

Usage:
    python rebuild-concept-column.py --package <prepared-package-dir>
    python rebuild-concept-column.py --package <dir> --check

``--check`` writes nothing and exits 1 when the column is out of date, so it can
gate a commit. Line endings of ``book.md`` are preserved exactly; only the third
column of each matched table row is rewritten, so the reference links cannot be
touched.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROW = re.compile(r"^\|\s*(\d+)\s*\|(.*?)\|(.*?)\|(.*?)\|\s*$")
CHAPTER_DIR = re.compile(r"^(\d+)-")


def load_columns(package: Path) -> tuple[dict[int, list[str]], list[str]]:
    """Map chapter index -> concept names, in the order concepts.json declares."""
    chapters = package / "chapters"
    if not chapters.is_dir():
        raise SystemExit(f"no chapters directory under {package}")
    columns: dict[int, list[str]] = {}
    problems: list[str] = []
    for directory in sorted(chapters.iterdir()):
        match = CHAPTER_DIR.match(directory.name)
        if not directory.is_dir() or not match:
            continue
        index = int(match.group(1))
        declaration = directory / "concepts.json"
        if not declaration.is_file():
            problems.append(f"chapter {directory.name}: no concepts.json")
            continue
        try:
            concepts = json.loads(declaration.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            problems.append(f"chapter {directory.name}: concepts.json unreadable ({exc})")
            continue
        if not isinstance(concepts, list):
            problems.append(f"chapter {directory.name}: concepts.json must be an array")
            continue
        names: list[str] = []
        for position, concept in enumerate(concepts):
            name = concept.get("name") if isinstance(concept, dict) else None
            if not isinstance(name, str) or not name.strip():
                problems.append(f"chapter {directory.name}: concepts[{position}] has no usable name")
                continue
            name = name.strip()
            if "|" in name:
                raise SystemExit(
                    f"chapter {directory.name}: concept name contains '|' and would break the table: {name!r}"
                )
            names.append(name)
        if index in columns:
            problems.append(f"two chapter directories share index {index}")
        columns[index] = names
    return columns, problems


def rebuild(package: Path, columns: dict[int, list[str]], write: bool) -> int:
    book_md = package / "book.md"
    if not book_md.is_file():
        raise SystemExit(f"no book.md under {package}")
    with open(book_md, encoding="utf-8", newline="") as handle:
        lines = handle.readlines()

    out: list[str] = []
    changed: list[tuple[int, int, int]] = []
    skipped: list[int] = []
    seen: set[int] = set()
    unmatched: set[int] = set()
    for line in lines:
        body = line.rstrip("\r\n")
        ending = line[len(body):]
        match = ROW.match(body)
        if not match:
            out.append(line)
            continue
        index = int(match.group(1))
        seen.add(index)
        if index not in columns:
            unmatched.add(index)
            out.append(line)
            continue
        link = match.group(4).strip()
        if not link.startswith("[") or "](" not in link:
            skipped.append(index)
            out.append(line)
            continue
        names = columns[index]
        before = [part.strip() for part in match.group(3).split(",") if part.strip()]
        rebuilt = f"| {index} |{match.group(2)}| {', '.join(names)} |{match.group(4)}|"
        out.append(rebuilt + ending)
        if before != names:
            changed.append((index, len(before), len(names)))

    if write and changed:
        with open(book_md, "w", encoding="utf-8", newline="") as handle:
            handle.writelines(out)
        with open(book_md, encoding="utf-8", newline="") as handle:
            if handle.readlines() != out:
                raise SystemExit("read-back mismatch: book.md was not written as expected")

    print(f"package                     {package}")
    print(f"chapters with concepts.json {len(columns)}")
    print(f"table rows matched          {len(seen)}")
    for index, before, after in changed:
        print(f"  row {index:>2}  {before:>3} -> {after} concepts")
    if changed:
        verb = "rows rewritten" if write else "rows stale (nothing written)"
        print(f"{verb}            {len(changed)}")
    else:
        print("rows rewritten              0  — column already matches concepts.json")
    for index in sorted(skipped):
        print(f"warning: row {index} does not look like a chapter-map row; left alone")
    for index in sorted(unmatched):
        print(f"warning: row {index} has no chapter directory; left alone")
    absent = sorted(set(columns) - seen)
    if absent:
        print(f"warning: chapters absent from the table: {absent}")
    return 1 if (changed and not write) else 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Rebuild book.md's concept column from each chapter's concepts.json.",
    )
    parser.add_argument("--package", required=True, type=Path, help="prepared package directory")
    parser.add_argument("--check", action="store_true", help="report only; exit 1 when out of date")
    args = parser.parse_args(argv)
    package = args.package.resolve()
    columns, problems = load_columns(package)
    for problem in problems:
        print(f"warning: {problem}", file=sys.stderr)
    return rebuild(package, columns, write=not args.check)


if __name__ == "__main__":
    raise SystemExit(main())
