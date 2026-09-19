---
name: book-reader
description: Build and publish compact book packages.
---

# Book Reader

Prepare a self-contained package with `book.json`, `book.md`, and one directory per declared chapter containing `source.md`, `guide.md`, and `concepts.json`. Preserve stable opaque IDs. Publish a valid package with `booksys packages import <prepared-package-dir>`, then confirm the result with `booksys doctor`.

Use `resources/templates/extraction-prompt.md` as the preparation checklist. Prepare the package outside the catalog, then publish it into `.booksys/content/books`; publication is the only way a package enters the catalog.

Harness discipline: use stable IDs from the prepared `book.json`; never invent an ID. If validation or import fails, inspect the reported package resource and repair it before retrying.
