## Runtime boundary

The active stage recorded by `.booksys/current.json` becomes the authoritative content root. The project root remains the system root for executable code, schemas, tests, and self-contained skill bundles. Runtime data such as operations, events, committed results, and projections lives under a dedicated `.booksys/runtime` data root.

## Content access

Add one resolver for the active stage and use it in analysis preparation, package validation, and projection/learning paths. Analysis selection reads v2 manifests and chapter resources rather than parsing `books/index.md`. Protocol and guidance files are loaded from `skills/` so deleting the legacy project skill directories does not remove runtime assets.

## V2 package authoring

The cutover retains a supported way to add content: a v2 importer accepts a prepared package directory, validates its strict manifest and provenance, and atomically publishes it beneath the active stage's `books/` root. It never reads or recreates the former Markdown workspace. The importer rejects an existing package slug unless an explicit replacement mode is introduced in a later change.

## Skill contract rewrite

Each canonical `skills/<name>/` bundle owns its config and reference material. Its documentation may describe historical provenance only when clearly marked as non-runnable history; active instructions must use the active-stage package catalog, `.booksys/runtime/learning/events.jsonl`, runtime projections, and bundled protocol/guidance assets. A reference scan enforces that removed top-level directories are not named as runtime paths.

## Removal boundary

After v2 checks pass, remove the rollback pointer, non-active migration snapshots, operation history, legacy data directories, compatibility adapters, and legacy pipeline tests. The CLI no longer exposes migration rollback or legacy-only commands.

## Verification

Run v2 package validation, unit/integration tests, `check_all.py`, OpenSpec validation, and representative `user.analyze`, `trainer.quiz`, and `coach.preview` preparations against the active stage. Verify no source/config/docs reference the removed compatibility paths except historical archive text.
