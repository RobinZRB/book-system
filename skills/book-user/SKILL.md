---
name: book-user
description: Analyze questions using the direct book catalog and bundled book packages.
---

# Book User

Start from `booksys books list` to see which packages are declared and where each one lives. Read `book.json` at each relevant path to see the title and declared chapter IDs and slugs, and read each relevant `book.md` for its chapter map and display titles. Choose books and chapters yourself; the runtime does not rank or select anything. When multiple books cover complementary dimensions of the question, load all of them by reading each selected book's `book.md`, chapter `source.md`, `guide.md`, and `concepts.json`. Before analyzing, disclose which books were loaded and the role each plays. Ask the user only when the choice between books would materially change the analysis or when the books conflict; otherwise do not pause for selection. Use `booksys books chapter <book-id> <chapter-id>` when you want one chapter's declared resource paths.


Use the selected book's framework as the analysis method. Keep book evidence, external evidence, and inference distinct, and state material uncertainty and applicability limits.

Keep book evidence, external evidence, and inference separate. State material uncertainty, applicability limits, and disconfirming conditions. For current facts, research only what matters and disclose source and date where available. Keep package and learning data unchanged.

Harness discipline: before a CLI call, read the current catalog declaration and use only its declared stable IDs. If a lookup fails, reread the declaration; never guess a replacement ID.

Catalog location: `booksys books list` resolves the catalog from the working directory, so it fails with a missing-catalog error in a workspace that only consumes books. First locate the book system root (the directory holding `.booksys/content/books`) — this skill ships `_book_system_root.txt` beside its `SKILL.md`, and that file's single line is this machine's absolute root — then point both flags at it: `cd "<root>" && booksys --project-root . --system-root . books list`. Never hardcode that root into this file or into a package: it is machine-private, and the Windows workstation and the Linux development box hold different paths. If it declares no packages, search the disk for `.booksys` directories rather than guessing package or chapter IDs.
