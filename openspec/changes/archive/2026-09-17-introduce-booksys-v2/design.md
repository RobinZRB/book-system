## Context

See `proposal.md` for motivation. The current project is a local, single-user knowledge system with four AI skills, Markdown knowledge packages, append-only mastery logs, derived indexes/maps, and five independent Python pipeline scripts. The current skills are concise, but their workflows expose filesystem layout, configuration ownership, parsing details, and post-write commands. The target must remain local-first, preserve all existing data, support `.agents` and `.workbuddy`, retain raw sources for audit, and improve engineering rigor without introducing a distributed platform.

The design uses the vocabulary of a deep Module: four skills are callers; `booksys` owns the external Interface; storage, scheduler, renderers, and migration are Implementation details behind that Seam. The Interface is also the primary test surface.

## Goals / Non-Goals

**Goals:**

- Give AI callers concrete, low-ambiguity operations while hiding paths, formats, write ordering, and recovery.
- Establish stable, versioned domain data and append-only learning history with deterministic projections.
- Make every authoritative write strict, idempotent, auditable, and recoverable.
- Preserve current user data and observed schedules through a staged, reversible migration.
- Keep the four skill discovery surfaces narrow while sharing one engineered runtime.
- Concentrate change in one Module so schema, scheduling, projection, and installation changes have high Locality.

**Non-Goals:**

- Multi-user accounts, network services, distributed locking, or concurrent writers beyond a local single-writer lock.
- A public plugin bus, configurable scheduler framework, vector database, MCP server, or background daemon.
- Replacing narrative Markdown with JSON or requiring users to read machine formats.
- Deleting raw source text, adopting an external source vault, or encrypting data as part of this change.
- Supporting `.claude` or `.opencode` installations in the core distribution.

## Decisions

### 1. Use a concrete operation workspace as the AI-facing Interface

The public CLI centers on concrete `prepare` intents and `commit`, plus explicit operator commands:

```text
booksys prepare reader.extract ...
booksys prepare reader.finalize ...
booksys prepare user.analyze ...
booksys prepare coach.preview ...
booksys prepare coach.complete ...
booksys prepare trainer.quiz ...
booksys prepare trainer.report ...
booksys commit <operation-id>
booksys doctor --strict
booksys migrate plan|apply
booksys project --check|--write
booksys skills install|doctor
```

`prepare` creates `.booksys/ops/<id>/request.json`, a minimal `context/`, `instructions.md`, `snapshot.json`, and, for writable operations, `result.schema.json`. The skill writes `result.json`; `commit` validates and applies it once.

This is preferred over exposing generic repositories or dozens of filesystem commands because it maximizes Leverage for the four common callers. A generic `apply/read/maintain` message Interface was considered, but it makes the AI learn action registries and storage-shaped queries. Direct file access was rejected because it recreates the present distributed protocol.

Internally, operations dispatch to typed private action/query handlers. Those handlers are not additional public Seams.

### 2. Implement one deep Python Module with private domain partitions

The package is organized by responsibility while exposing only the operation Interface:

```text
src/booksys/
  operations/
  domain/
  packages/
  learning/
  storage/
  projections/
  migration/
  installation/
```

`domain` defines stable identities and typed facts; `packages` owns manifests and provenance; `learning` owns EMT/mastery reductions and FSRS; `storage` owns JSON/JSONL, staging, locks, and atomic replacement; `projections` owns Markdown rendering; `migration` owns v1 import; and `installation` owns supported harness targets.

This avoids replacing one 1,189-line script with another. Internal partitions improve Locality, but they remain private so callers and tests cannot depend on implementation details.

### 3. Separate `system_root` and `data_root` with one root configuration

`system_root` contains version-controlled code, schemas, templates, skills, fixtures, and OpenSpec artifacts. `data_root` contains private raw texts, packages, events, projections, staging, and operation workspaces. A root config stores root selection, categories, and protocol registry. Coach and trainer keep only their genuine policy settings.

Resolution order is explicit command option, root configuration, then the project-local compatibility default. Configuration parse errors fail closed. Machine-specific Python paths and policy prose are removed from feature configs.

An environment-variable-only design was rejected because it is difficult for local users to inspect and migrate. Keeping four independent configs was rejected because it preserves cross-skill coupling.

### 4. Use versioned facts and deterministic Markdown projections

The authoritative split is:

- JSON/JSONL: manifests, identities, concepts, relations, reading events, review events, and scheduler policy metadata.
- Markdown: narrative chapter reference and chapter guide content.
- Projections: book registry, concept indexes, glossary, reading plan/prep views, review log, mastery map, and due reports.

Every projection carries renderer/version metadata outside user-authored content and is generated to staging before atomic replacement. `project --check` renders in memory or staging and reports drift; it never repairs. `project --write` is the only explicit repair path.

Making every chapter document JSON was rejected because it degrades human and AI readability. Keeping Markdown tables as facts was rejected because escaping, mutable names, and multiple parsers make the data contract fragile.

### 5. Use package manifests, stable IDs, and provenance

Each formal book receives a versioned manifest listing authoritative and projected resources with roles, byte sizes, digests, and generator metadata. IDs are immutable opaque values stored with human-readable slugs, names, and aliases. Category is mutable metadata rather than identity.

Existing IDs are assigned deterministically during migration and persisted in an ID map so retrying the same migration is stable. Future creation persists generated IDs once; it does not recompute them from mutable names.

Concepts, relations, evidence, and claims record raw source SHA-256 plus character start/end offsets and an evidence class. Reliable page locators are optional. Raw files remain in `data_root` for this change.

### 6. Use append-only learning events and immediate FSRS for observed new reviews

Reading and review events have versioned envelopes, stable aggregate IDs, timezone-aware occurrence time, idempotency keys, and typed payload versions. Corrections append compensating/superseding events. Derived mastery and schedules are checkpoints/projections, not editable facts.

The project adds a pinned `fsrs` dependency and records scheduler and parameter versions. Desired retention defaults to `0.90`. A review records both pedagogical evidence and scheduling evidence. Objective EMT failure forces Again; objective pass accepts the user's pre-feedback Hard/Good/Easy rating.

Legacy history is not rewritten into invented ratings. Existing due dates remain active until each concept's next real review, when a complete event is recorded and FSRS takes over subsequent scheduling. This satisfies immediate adoption without changing current due queues at migration time.

A permanently pluggable scheduler Interface was rejected: only FSRS is a future scheduler after takeover. The legacy calculation exists solely inside the migration compatibility path and does not justify a public extension framework.

### 7. Stage writes and commit atomically

`commit` validates the operation snapshot and result, acquires a local single-writer lock, writes facts/events to staging or a recoverable journal, renders affected projections, validates the staged result, and atomically swaps the committed files. A receipt records the operation identity, new revision, affected resources, projection state, and diagnostics.

For append-only event files, commit writes a fully validated event and fsyncs before advancing the manifest/checkpoint. Recovery detects an incomplete journal and either completes a validated projection swap or discards uncommitted staging. Identical retries return the prior receipt; the same key with different content fails.

A database transaction was considered but rejected for v2 because a local JSON/JSONL implementation can provide the required single-user guarantees with lower migration and operational cost.

### 8. Keep real Adapter Seams only

- The pinned FSRS library is isolated behind a private adapter so third-party types do not enter domain events.
- Legacy Markdown import and v2 canonical storage are two real adapters during migration.
- `.agents` and `.workbuddy` are two real installation targets.
- Filesystem and clock are privately substitutable for tests, preferably using real temporary directories and a fixed clock.
- Search remains a scan/thin-index implementation. An internal search Seam is introduced only if FTS5 is actually added later.

No vector, MCP, object-store, or generic plugin seams are created speculatively.

### 9. Build and install self-contained skill bundles

Each canonical skill contains its `SKILL.md`, referenced guidance, and assets at skill-root-relative paths. The skill documents trigger boundaries, semantic responsibilities, and exact `booksys` commands; it does not repeat storage layout or write protocol.

Installation is per skill. Windows uses verified junctions, other supported platforms use symbolic links, and copying requires an explicit option. A managed-link receipt records bundle digest and target. Real directory collisions stop without deletion. OpenSpec-managed `.agents/skills/openspec-*` entries remain untouched.

### 10. Treat mechanical tests and behavioral evals as complementary gates

Tests cross the public operation Interface with temporary `data_root` fixtures. They cover schema failures, provenance, stale workspaces, idempotency, fault recovery, deterministic rendering, projection deletion/rebuild, migration parity, FSRS sequences, and installer collisions. Focused pure tests are permitted for reducers and schemas, but callers do not test past the external Interface.

Each skill also has 3-5 representative behavioral evals. Hard constraints have zero tolerance; soft quality measures compare success, traceability, token use, latency, and blind preference against the accepted baseline. Existing shallow tests are removed only after replacement coverage exists.

## Risks / Trade-offs

- [Migration may expose unsupported or ambiguous legacy rows] -> Plan migration first, require explicit mapping for ambiguity, preserve originals, and block cutover until strict validation and parity pass.
- [Operation workspaces add two-phase ceremony] -> Keep concrete task commands, generate concise instructions, make read-only operations complete after preparation, and clean expired workspaces safely.
- [The deep Module could become a god file] -> Enforce private domain partitions and test the external Interface while prohibiting callers from importing internal modules.
- [JSON facts are less convenient to hand-edit] -> Keep narrative Markdown authoritative, provide validated correction/import operations, and maintain readable projections.
- [FSRS changes future due dates] -> Preserve existing due dates until a real next review, record versions and policy, and include scheduling goldens.
- [Projection generation may fail after facts are valid] -> Stage and validate required projections before the atomic commit; allow explicit rebuild from unchanged facts.
- [External `data_root` complicates portability] -> Keep one inspectable root config, provide doctor diagnostics, and preserve the project-local compatibility default for one cycle.
- [Skill behavior can regress despite passing code tests] -> Gate releases on zero-tolerance behavioral evals and keep accepted baselines versioned.

## Migration Plan

1. Add packaging metadata, root configuration schema, typed domain contracts, and read-only strict doctor without changing current writes.
2. Add behavior baselines and mechanical characterization tests for existing packages, projections, installer behavior, and learning state.
3. Implement package manifests, stable ID assignment, structured concepts/relations, provenance validation, renderers, and `project --check` in shadow mode.
4. Implement append-only reading/review events, FSRS for new observed reviews, and legacy schedule takeover logic in shadow mode.
5. Implement concrete `prepare`/`commit` workspaces, staging, idempotency, recovery, and receipts; convert legacy scripts into parity-tested adapters.
6. Build self-contained skills and the per-skill installer for `.agents` and `.workbuddy`; keep existing installations until target validation passes.
7. Run `migrate plan` across both formal books, 31 chapters, reading state, and mastery state; resolve every ambiguity and validate source spans.
8. Apply migration into staging, render all projections, compare semantic and scheduling parity, run unit/integration/eval gates, and record the plan digest.
9. Atomically switch to v2 facts and new skill bundles while retaining the complete v1 data and old entry adapters for one compatibility cycle.
10. After the rollback window and zero observed legacy calls, archive migration evidence and use a separate OpenSpec change to remove compatibility adapters and unsupported generated integrations.

Rollback before step 9 discards staging only. Rollback during the compatibility cycle restores the v1 data pointer and prior skill links; v2 events collected after cutover must be exported and reconciled rather than silently discarded.
