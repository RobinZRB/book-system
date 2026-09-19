## Context

The current runtime resolves the active v2 stage successfully, but `RootConfig` still carries a compatibility flag, the CLI still exposes a baseline generator that emits `v1-manifest.json`, and active content retains migration-only v1 labels. The completed cutover requires a clean v2 surface without deleting authoritative books, raw sources, v2 events, or projections.

## Goals / Non-Goals

**Goals:**

- Remove v1 compatibility behavior and commands from executable code.
- Normalize active v2 metadata and remove only migration artifacts proven not to be authoritative runtime inputs.
- Establish automated checks that detect v1 reintroduction across runnable code, active data, skills, evaluations, and operator documentation.

**Non-Goals:**

- Rewrite book content, stable entity identifiers, event history, or projections.
- Delete OpenSpec archives, which are immutable historical audit records.
- Introduce a new storage backend or modify the v2 package format beyond provenance-label normalization.

## Decisions

### Treat `.booksys` as the canonical default runtime root

Remove the compatibility flag and its legacy terminology, but retain the project-local `.booksys` default so existing v2 projects continue to operate. Requiring an external data root would create an unnecessary data migration and is not needed to eliminate v1 behavior.

### Remove the baseline command instead of porting it

The baseline generator is a characterization tool for the retired layout and its output explicitly uses a v1 name. Remove its CLI registration, implementation module, and tests rather than creating a v2 version without an identified operational consumer.

### Normalize metadata only through validated, deterministic transformations

Before changing active manifests, id maps, plans, or events, inventory every v1-labelled field and its consumers. Preserve stable IDs and content bytes where required; rewrite only non-identity provenance labels and regenerate/check package metadata as needed. Delete `legacy-due.json` only after cross-checking that its entries are represented by v2 events or deterministic projections.

### Scope residue scans to runnable and active surfaces

The scan covers source, tests, skills, eval assets, active `.booksys` data, and operator documentation. It explicitly excludes `openspec/changes/archive`, because historical specifications are not executable and must remain auditable.

## Risks / Trade-offs

- [A v1-labelled field participates in an identity or digest] → Map consumers first, make a fixture copy, and require strict validation plus stable-ID assertions before replacing the active value.
- [Legacy due data contains information absent from v2 events] → Stop deletion, surface the mismatch, and migrate the missing evidence through a separately reviewed v2 event path.
- [A consumer relies on the root compatibility flag] → Replace it with explicit v2-root semantics and cover default and externally configured root cases in tests.
- [Broad text scanning produces historical false positives] → Restrict enforcement to the defined runnable/active paths and retain an explicit archive exclusion.

## Migration Plan

1. Add failing tests for the v2-only CLI, root resolution, metadata scan, and active learning-state invariants.
2. Remove the baseline command/module and compatibility flag; preserve v2 default-root behavior.
3. Inventory and normalize active v2 metadata, then remove validated obsolete migration artifacts.
4. Run strict package health, projection checks, full tests, evaluation suite, and the residue scan before accepting the cleanup.
