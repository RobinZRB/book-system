## Why

The current four-skill architecture has sound role and write-permission boundaries, but each skill and pipeline script still needs to understand paths, Markdown table formats, configuration ownership, projection order, and recovery steps. This makes AI-driven execution fragile: incomplete book packages can pass validation, project-level skill installation conflicts with OpenSpec-owned skill directories, learning history is keyed by mutable concept names, and the existing review log cannot support the promised lossless FSRS migration.

Now is the least expensive time to establish a durable contract: the system contains only two formal books and 31 chapters, while existing data can still be migrated and compared in full. The change will preserve the four focused skills while moving deterministic correctness behind one engineered `booksys` module.

## What Changes

- Introduce an AI-facing `booksys` operation interface centered on `prepare`, `commit`, and read-only `doctor`, with explicit maintenance commands for migration, projection, and skill installation.
- Separate version-controlled `system_root` assets from configurable private `data_root` content, while retaining the current in-project layout as a compatibility default for one migration cycle.
- Introduce versioned book-package manifests, immutable internal IDs with human-readable aliases, resource hashes, and source provenance down to raw-text character spans.
- Make structured concept/relation data and append-only reading/review events the machine sources of truth; keep narrative content in Markdown and make indexes, glossaries, reading views, review logs, and mastery maps deterministic projections.
- Integrate a pinned FSRS implementation for new review events with default desired retention `0.90`; preserve existing due dates and let each legacy concept enter FSRS only after its next real review.
- Capture user recall rating, EMT evidence, objective pass/fail, confidence, scheduler version, and final scheduling rating without fabricating missing historical ratings.
- Build self-contained skill bundles whose instructions call `booksys`, and install `book-reader`, `book-user`, `book-coach`, and `book-trainer` individually into `.agents` and `.workbuddy` so they can coexist with OpenSpec skills.
- Replace permissive and mutating health checks with strict, read-only validation; add migration parity tests, deterministic projection tests, scheduler tests, installer tests, and behavioral evals for the four skills.
- Preserve legacy scripts and Markdown inputs as compatibility adapters for one explicit deprecation cycle; remove their business logic and direct-write paths after migration criteria are met.
- Remove unsupported `.claude` and `.opencode` generated integrations from the core distribution, Python bytecode caches, duplicated sample fixtures, and hard-coded historical test counts.
- **BREAKING**: after v2 cutover, machine-generated Markdown projections are no longer valid write inputs; authoritative changes must use `booksys` operations or validated structured source files.

## Capabilities

### New Capabilities

- `booksys-operations`: AI-oriented operation workspaces, deterministic commits, strict diagnostics, root/config resolution, projections, and legacy command adapters.
- `knowledge-packages`: Versioned package manifests, stable identities, structured knowledge resources, provenance, validation, and deterministic Markdown projections.
- `learning-state`: Append-only reading/review events, EMT and mastery state, FSRS scheduling, legacy takeover behavior, and learning projections.
- `skill-distribution`: Self-contained four-skill bundles, per-skill cross-platform installation into `.agents` and `.workbuddy`, and behavioral evaluation requirements.

### Modified Capabilities

None. The project has no existing OpenSpec capability specifications; the four entries above establish the initial behavioral contract.

## Impact

- Affected implementation: all five current pipeline scripts, `check_all.py`, `setup-skills.bat`, four skill bundles, four skill/config directories, book package templates, reading/mastery storage, and generated indexes/maps.
- New implementation surface: a Python package and unified CLI under `booksys`, JSON Schemas, migration tooling, typed operation/result contracts, FSRS adapter, projection renderers, and eval fixtures.
- Data migration: all existing formal books and 31 chapters, current reading state, and current mastery history are migrated through staging, compared against legacy outputs, and atomically cut over with a rollback window.
- Dependencies: add a pinned supported `fsrs` Python package and project packaging/lock metadata; no vector database, MCP server, plugin bus, multi-user store, or distributed service is introduced.
- Distribution: `.agents` and `.workbuddy` are the supported harness targets. Private raw texts and learner data remain outside default distributable artifacts.
