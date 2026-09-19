## 1. Establish the migration baseline

- [x] 1.1 Record the current package identities, chapter identities, concept identities, learning-event fixtures, and representative FSRS outputs; verify the existing full test suite passes before migration work. Baseline recorded; the suite passed before migration began.
- [x] 1.2 Define the small `book.json`, `book.md`, `source.md`, `guide.md`, and `concepts.json` fixture format; verify each required field and path rule has a failing and passing validation test. Implemented in `packages/small.py` with focused tests.

## 2. Build the direct book catalog

- [x] 2.1 Replace rich-manifest validation with small-package validation while retaining path containment, non-empty resource, and stable-ID checks; verify focused package validation tests pass. Implemented in `src/booksys/packages/small.py` and importer integration.
- [x] 2.2 Add catalog discovery and direct book/chapter/concept lookup without natural-language query inputs; verify list, exact-ID lookup, unknown-ID rejection, and rejection of display names. Implemented in `src/booksys/catalog.py`, `src/booksys/cli.py`, and focused catalog tests.
- [x] 2.3 Update package publication to validate and atomically publish a small package into the canonical direct catalog; verify overwrite rejection and successful publication. Covered by `tests/test_small_importer.py`.
- [x] 2.4 Convert both active books into the small format with an explicit stable-ID mapping; verify every declared source, guide, and concept resource is reachable and old learning fixtures still resolve their IDs. Converted into `.booksys/content/books` — 2 books, 31 chapters, 876 concepts.

## 3. Isolate the learning module

- [x] 3.1 Introduce a single learning service that encapsulates append-only events, reducers, and FSRS; verify replay produces the characterized status and due fixtures. Implemented in `src/booksys/learning/service.py`.
- [x] 3.2 Add `learn status`, `learn complete`, `learn due`, and `learn review` commands with declared-ID validation; verify invalid IDs make no write and valid coach/trainer writes remain isolated. Implemented in `src/booksys/cli.py`.
- [x] 3.3 Make derived learning state private and rebuildable rather than a required public file contract; verify that no cache is needed to reconstruct progress, mastery, or due results. The learning service derives status and due directly from the append-only stream.

## 4. Move semantic analysis into book-user

- [x] 4.1 Rewrite book-user guidance and protocol assets to use direct catalog resources, AI-owned source selection, evidence/inference separation, uncertainty disclosure, and proportionate current-fact research; verify no executable instruction requires analysis workspaces or retry rationale fields. Updated `skills/book-user/SKILL.md`.
- [x] 4.2 Retire `analysis_context.py` and all `user.analyze` keyword-routing, analysis-plan, assurance, external-fact-package, and read-only workspace behavior; verify the CLI has no analysis preparation command and direct catalog queries cover skill needs. Removed module and workspace branch.
- [x] 4.3 Keep domain-specific checklists, including investment-oriented Gate and risk prompts, inside selected book protocols rather than a separate system capability; verify representative answers retain source basis and material caveats without fixed runtime states. Guidance now leaves these decisions to book protocols and AI reasoning.

## 5. Route the four skills through the new seams

- [x] 5.1 Update book-reader to emit and validate the small package format; verify a prepared fixture can be published and cataloged. Updated skill guidance and compact importer.
- [x] 5.2 Update book-coach to read direct package resources and use only status and completion commands; verify it cannot modify packages or review events. Updated skill guidance and learning service.
- [x] 5.3 Update book-trainer to read declared concepts and use only due and review commands; verify objective-failure rating behavior and FSRS scheduling remain unchanged. Updated skill guidance and preserved event/scheduler contracts.
- [x] 5.4 Replace marker-only skill evaluations with an offline contract check that verifies bundle presence, the declared runtime command per skill, and catalog integrity. Updated all skill eval contracts and cases.

## 6. Cut over safely

- [x] 6.1 Update CLI help, README, runtime documentation, and schemas to describe the direct catalog and learning interface; verify documentation contains no active-stage, generic-operation, or analysis-plan instruction. Updated README, RUNTIME.md, the four skill bundles, and the eval contracts.
- [x] 6.2 Run catalog validation, `doctor`, all unit tests, and manual coach and trainer smoke flows against the migrated books; verify all acceptance commands succeed. `18` unit tests, `doctor`, and catalog checks pass.
- [x] 6.3 Remove retired operation, analysis, stage-pointer, projection, installer, and no-longer-consumed derivative artifacts; verify the active catalog and learning commands work with those paths absent. `src/booksys/installation/`, `operations/`, `projections/`, `.booksys/installations/`, the four `skills/*/config.json`, and the duplicated `guidance.md` files are gone.

## 7. Remove remaining runtime matching and surface

- [x] 7.1 Remove identifier matching from the catalog: `select_book`, `locate_chapter`, and `locate_concept` accept stable IDs only, never a title, name, or alias; `CatalogError` no longer carries candidates and the CLI no longer prints them. Verify that passing a display name is rejected and that no candidate list is produced. Implemented in `src/booksys/catalog.py` and `src/booksys/cli.py`.
- [x] 7.2 Remove the scope arguments that only existed to narrow a match: `learn status` no longer filters per book, and `learn review` takes a concept ID alone. Verify status reports the whole stream and review resolves the owning chapter from the concept ID.
- [x] 7.3 Remove idempotency-related failure modes: an event without an explicit idempotency key is always new, so a repeated chapter completion appends a further reading event; a repeated identical review appends a further review event; a repeated explicit key is ignored instead of raising. Verify repeated coach and trainer calls succeed.
- [x] 7.4 Wire FSRS state through the seam so scheduling resumes from recorded history: the adapter serialises state to round-trippable types and accepts its own recorded state back, and `review_concept` passes the concept's previous state. Verify stability grows across reviews with a real gap and stays constant when state is withheld.
- [x] 7.5 Remove the installer, the release archive, and the config-writing command, and stop grafting `.booksys/content` into distributions. Verify `release` and `config init` are rejected by the CLI, `doctor --strict` is rejected, and no build path copies the catalog.
- [x] 7.6 Remove declared-but-unread fields and stale text: `RootConfig.source`, `list_books`' `overview` and `book_path`, the `write_default_config` writer, the duplicated learning `__init__` re-exports, and the `domain` docstring that still referred to the retired operation interface.
- [x] 7.7 Converge the design documents with the implementation: drop the superseding-correction requirement, the per-claim source-reference validation, the installations and adapter checks in `doctor`, the zero-tolerance release gate claim, the `[book]` status argument, and the alias/ candidate language; delete the deployed spec that still described `user.analyze` workspaces.

## 8. Remove the packaging surface and the redundant declaration fields

- [x] 8.1 Remove the build-and-ship surface: delete `MANIFEST.in` and `src/booksys/py.typed`, and drop `[build-system]`, `[tool.setuptools.packages.find]`, `[tool.setuptools.package-data]`, and `[project.scripts]` from `pyproject.toml`. Verify nothing in the tree references them and that `pyproject.toml` retains only the project identity block.
- [x] 8.2 Remove the declaration field that repeated the book title: drop `aliases` from `book.json` and the matching validation in `src/booksys/packages/small.py`. Verify the active packages load without it.
- [x] 8.3 Remove the declaration field that was never filled: drop `overview` from `book.json`, which the `book.md` narrative already carries. Verify the active packages load without it.
- [x] 8.4 Remove the declaration field that repeated the chapter slug: drop `title` from every chapter entry in `book.json`, leaving chapter IDs and slugs. Verify the `book.md` chapter map remains the display-title source.
- [x] 8.5 Keep concept `aliases`, which record real alternate names, and keep the catalog read of `book.md` for chapter display titles. Verify 413 concepts still carry aliases and that the four skill bundles and `extraction-prompt.md` describe the reduced declaration.
- [x] 8.6 Remove the residual packaging declarations too: delete `pyproject.toml` and `requirements.lock`, which no tool in the tree reads and which duplicate information already held elsewhere (the version in `src/booksys/__init__.py`, the FSRS pin in `learning/scheduler.py`). Record the Python floor and the dependency in `RUNTIME.md` so the removed files carry no unique information. Verify the CLI and the tests still pass with no file declaring a build.
- [x] 8.7 Remove the evaluation assets and retire the requirement that mandated them: `evals/` held four skill contract files and one runner, and no runtime path read any of them. Delete the directory, drop the "Offline contract check" requirement from the `skill-distribution` spec, and record the retirement in the design's Retired surface. Verify no active document names a deleted eval path and that `doctor` still reports catalog integrity, which is the part the runner duplicated.
