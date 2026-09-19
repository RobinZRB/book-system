---
name: book-coach
description: Guide a reader using compact book packages and append-only reading events.
---

# Book Coach

Read declared package resources through `booksys books chapter <book-id> <chapter-id>`. Use `booksys learn status` for progress and `booksys learn complete <book-id> <chapter-id>` to record that a chapter was read.

Arguments are stable IDs taken from the package declaration. Resolve a book or chapter title to its ID yourself by reading `book.json`; the runtime refuses to guess. Each completion appends one reading event, so a re-read is recorded as a further event rather than replacing the earlier one.

Use `resources/reference/METHODOLOGY.md` for method guidance. Never modify package content or review events.

Harness discipline: before recording completion, reread the selected package declaration and use its exact IDs. For a transport retry of the same completion, reuse one `--idempotency-key`; use a new key for an intentional re-read.
