## Why

The v2 migration package is complete and selected by the active pointer, but runtime reads still fall back to the legacy `books/`, `reading/`, and `mastery/` layout and retain rollback/adapter behavior. This leaves the project in a compatibility state instead of making v2 the single authoritative release.

## What Changes

- **BREAKING** Make the active v2 migration stage the only runtime content root.
- Route analysis, package validation, learning events, projections, and skill operations through v2 storage.
- Move runtime guidance/protocol assets into the canonical `skills/` distribution and remove legacy pipeline adapters.
- Replace the removed legacy pipeline with a v2 package importer that validates and publishes a self-contained package into the active v2 content root.
- Rewrite the four skill bundles and their configurations so every documented runtime path points to v2 content, v2 event/projection state, or bundled resources.
- Remove rollback commands, historical migration snapshots, operation history, and legacy data directories after parity verification.
- Update documentation and tests to describe and enforce the v2-only contract.

## Capabilities

### New Capabilities

- `v2-only-runtime`: The project runs exclusively from the active v2 package and event store.

### Modified Capabilities

- `booksys-operations`: Resolve active v2 content and learning roots without compatibility fallback or rollback.
- `knowledge-packages`: Treat the active v2 package set as authoritative and remove legacy-compatible staging behavior.
- `learning-state`: Read and write v2 events/projections without legacy takeover logic.
- `skill-distribution`: Keep runtime guidance self-contained under `skills/` and remove legacy pipeline entry points.

## Impact

Affected areas include `src/booksys/config.py`, analysis and workspace preparation, migration/rollback CLI paths, skill resources/configuration, tests, README/MIGRATION documentation, and project data directories. This is an intentional breaking cutover; the legacy data and adapters will no longer be recoverable after cleanup.
