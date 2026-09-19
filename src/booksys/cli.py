from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from . import __version__
from .catalog import CatalogError, catalog_root, list_books, locate_chapter, read_declaration, select_book
from .config import ConfigError, resolve_roots
from .learning.service import complete_chapter, due as learning_due, review_concept, status as learning_status
from .packages.importer import import_package
from .packages.small import validate_book_md_links, validate_small_package
from .paths import runtime_root


def _parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="booksys", description="Compact local-first book knowledge runtime")
    p.add_argument("--version", action="version", version=__version__)
    p.add_argument("--project-root", type=Path, default=Path.cwd(), help="root that holds .booksys (default: working directory)")
    p.add_argument("--data-root", type=Path, help="root for private learning state (default: project root)")
    p.add_argument("--system-root", type=Path, help="root that holds the book catalog (default: project root)")
    sub = p.add_subparsers(dest="command", required=True)
    sub.add_parser("doctor", help="validate the catalog and the learning event stream")

    books = sub.add_parser("books", help="locate declared package resources")
    bs = books.add_subparsers(dest="action", required=True)
    bs.add_parser("list", help="list declared book identities and locations")
    show = bs.add_parser("show", help="print one declaration by book id")
    show.add_argument("book_id")
    chapter = bs.add_parser("chapter", help="print one chapter's declared resource paths")
    chapter.add_argument("book_id")
    chapter.add_argument("chapter_id")

    learn = sub.add_parser("learn", help="read and record learning state")
    ls = learn.add_subparsers(dest="action", required=True)
    ls.add_parser("status", help="show reading and mastery state")
    complete = ls.add_parser("complete", help="append one reading event")
    complete.add_argument("book_id")
    complete.add_argument("chapter_id")
    complete.add_argument("--idempotency-key", help="stable harness request key; reuse only when retrying the same request")
    review = ls.add_parser("review", help="append one review event and schedule the next one")
    review.add_argument("concept_id")
    review.add_argument("payload", help="JSON object with the objective assessment fields")
    review.add_argument("--idempotency-key", help="stable harness request key; reuse only when retrying the same request")
    ls.add_parser("due", help="show concepts whose latest review is due")

    packages = sub.add_parser("packages", help="publish compact book packages")
    ps = packages.add_subparsers(dest="action", required=True)
    imp = ps.add_parser("import", help="validate and publish one prepared package")
    imp.add_argument("source", type=Path)
    return p


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        roots = resolve_roots(args.project_root, system_root=args.system_root, data_root=args.data_root)
        if args.command == "doctor":
            return _doctor(roots)
        if args.command == "books":
            if args.action == "list":
                result = {"books": list_books(roots)}
            elif args.action == "show":
                book = select_book(roots, args.book_id)
                result = {**book, "declaration": read_declaration(book["package_path"])}
            else:
                result = locate_chapter(roots, args.book_id, args.chapter_id)
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return 0
        if args.command == "learn":
            if args.action == "status":
                result = learning_status(roots)
            elif args.action == "complete":
                result = complete_chapter(roots, args.book_id, args.chapter_id, idempotency_key=args.idempotency_key)
            elif args.action == "review":
                result = review_concept(roots, args.concept_id, json.loads(args.payload), idempotency_key=args.idempotency_key)
            else:
                result = {"due": learning_due(roots)}
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return 0
        if args.command == "packages":
            print(json.dumps(import_package(roots, args.source), ensure_ascii=False, indent=2))
            return 0
    except (ConfigError, CatalogError, ValueError, FileNotFoundError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "error", "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    return 0


def _doctor(roots) -> int:
    diagnostics: list[dict[str, object]] = []
    catalog = catalog_root(roots)
    count = 0
    if catalog.is_dir():
        for package in sorted(p for p in catalog.iterdir() if p.is_dir()):
            count += 1
            diagnostics.extend({"path": str(package), "error": error} for error in validate_small_package(package))
            diagnostics.extend(
                {"path": str(package / "book.md"), "error": error}
                for error in validate_book_md_links(package, roots.system_root)
            )
        try:
            list_books(roots)
        except CatalogError as exc:
            diagnostics.append({"path": str(catalog), "error": str(exc)})
    else:
        diagnostics.append({"path": str(catalog), "error": "book catalog is missing"})
    diagnostics.append({"code": "book_packages", "count": count})

    event_count = 0
    event_path = runtime_root(roots) / "learning" / "events.jsonl"
    if event_path.is_file():
        from .learning.events import EventStreamError, iter_event_records
        from .learning.validation import validate_event
        try:
            for line_no, event in iter_event_records(event_path):
                event_count += 1
                diagnostics.extend(
                    {"path": str(event_path), "line": line_no, "error": error}
                    for error in validate_event(event)
                )
        except (OSError, EventStreamError) as exc:
            diagnostic = {"path": str(event_path), "error": str(exc)}
            if isinstance(exc, EventStreamError):
                diagnostic["line"] = exc.line_no
            diagnostics.append(diagnostic)
    diagnostics.append({"code": "learning_events", "count": event_count})
    diagnostics.append({"code": "runtime_root", "path": str(runtime_root(roots))})

    bad = any(item.get("error") for item in diagnostics)
    print(json.dumps({"status": "error" if bad else "ok", "diagnostics": diagnostics}, ensure_ascii=False, indent=2))
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
