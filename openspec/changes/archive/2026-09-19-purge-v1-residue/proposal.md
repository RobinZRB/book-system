## Why

The v2 cutover removed the legacy workspace layout, but the repository still exposes v1 compatibility behavior, a v1 baseline command, and v1-labelled migration artifacts. With v2 operating cleanly, those remnants obscure the supported contract and preserve an unintended compatibility surface.

## What Changes

- Remove the `compatibility_default` root mode while retaining the existing v2 `.booksys` runtime root as the default project-local data location.
- **BREAKING** Remove the `booksys baseline` CLI command and its v1 manifest generator.
- Remove v1-labelled evaluation baselines and migration-only metadata from the active v2 catalog, while retaining the authoritative package content, learning events, and projections.
- Remove the legacy-due migration artifact only after verifying its due-state information is represented by the v2 event stream/projections.
- Update tests, documentation, health/reference scans, and release checks so they reject reintroduction of v1 paths, commands, metadata, or compatibility behavior in runnable surfaces and active v2 data. OpenSpec archival history remains an immutable audit record.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `booksys-operations`: root resolution and the public CLI must expose only the v2 runtime contract.
- `knowledge-packages`: active package metadata must be v2-native and free of v1 migration labels while retaining valid provenance.
- `learning-state`: active learning state must retain only authoritative v2 events and projections, without legacy due-state artifacts.
- `skill-distribution`: evaluation and distribution metadata must no longer depend on a v1-labelled baseline.
- `v2-only-runtime`: the release must have no runnable compatibility paths or v1-labelled runtime residue.

## Impact

Affected areas include `src/booksys/config.py`, `src/booksys/cli.py`, `src/booksys/baseline.py`, evaluation manifests/runner, v2 package manifests and migration metadata under `.booksys/content`, tests, `check_all.py`, and migration documentation. The change must not delete book packages, raw sources, append-only v2 learning events, or current projections.
