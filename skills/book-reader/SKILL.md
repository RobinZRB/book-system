---
name: book-reader
description: Build and publish compact book packages.
---

# Book Reader

Prepare a self-contained package with `book.json`, `book.md`, and one directory per declared chapter containing `source.md`, `guide.md`, and `concepts.json`. Preserve stable opaque IDs. Publish a valid package with `booksys packages import <prepared-package-dir>`, then confirm the result with `booksys doctor`.

Use `resources/templates/extraction-prompt.md` as the preparation checklist. Prepare the package outside the catalog, then publish it into `.booksys/content/books`; publication is the only way a package enters the catalog.

Settle chapter granularity before extracting anything, because a chapter's `source.md` has to stay small enough for one subagent to hold it whole — treat roughly 60 KB as the ceiling. A translated book can concentrate half its length in one nominal chapter (`Poor Charlie's Almanack`'s fourth chapter held 670 KB, 54% of the book) and the fix is to promote that chapter's own internal sections to chapters. Front matter — preface, acknowledgements, reading guide — becomes chapters on the same terms as body text: short, but not a separate class of resource. Slugs are safe directory names with no spaces and no `/`, because `book.md` links are matched by `\]\(\s*([^)\s]+)` and a space breaks them.

Extract chapter by chapter with one subagent per chapter, keeping chapter text out of the orchestrator's context. Write the per-chapter brief once — layout, the `guide.md` template, the `concepts.json` rules, the self-check command — into a file the subagents read, then hand each subagent only its slug, display title, chapter directory, the two files it writes, and one line of subject-matter orientation. Run them in batches of about ten and require each to report its self-check output. Chapter display titles belong to the chapter map in `book.md`, never to `book.json`.

The catalog is one namespace: `books list` rejects a duplicate `book_id`, `chapter_id`, or `concept_id` across every published package, so generate IDs opaquely — `book:` / `chapter:` / `concept:` plus `secrets.token_hex(12)` — and never sequence or reuse them. Chapter-index links in `book.md` are written relative to the book-system root as `.booksys/content/books/{slug}/chapters/{chapter_dir}/source.md`, and `doctor` runs `validate_book_md_links`, so a wrong target is reported rather than tolerated. Generate the chapter map's concept column from each chapter's `concepts.json` instead of writing it by hand; otherwise it drifts the first time a concept is renamed.

Converge concept names before the first import, because a published package is immutable and `packages import` offers neither overwrite nor removal. One idea left under a separate ID in every chapter that mentions it makes `book-trainer` ask the same question repeatedly, so give one idea one ID. An ID cannot be declared twice, so converging means deleting the duplicate entries and folding their names into the keeper's `aliases`. Keep the entry in the chapter that enumerates the concept systematically; otherwise in the earliest body chapter that treats it substantively, with front matter as a home only when it is the sole place the concept appears. Leave qualified, chapter-specific applications alone — they carry their own training value. To revise an already published package, delete `.booksys/content/books/<name>` and import again, checking `learn status` first: changing concept IDs orphans review history.

Harness discipline: use stable IDs from the prepared `book.json`; never invent an ID. If validation or import fails, inspect the reported package resource and repair it before retrying.
