## 1. Baseline and Project Foundation

- [x] 1.1 Inventory the two formal books, 31 chapters, learning-state files, current projections, legacy commands, and installed skill links into a versioned sanitized baseline manifest; verify the inventory counts and digests reproduce on a second run.
- [x] 1.2 Add characterization tests for current package discovery, generated Markdown, reading/mastery behavior, and legacy command exit behavior; verify the tests pass against the untouched v1 fixtures.
- [x] 1.3 Add 3-5 accepted baseline behavioral evals for each of `book-reader`, `book-user`, `book-coach`, and `book-trainer`; verify all zero-tolerance rules and baseline measurements are recorded.
- [x] 1.4 Create Python packaging and lock metadata with a pinned supported FSRS dependency and a `booksys` console entry point; verify a clean environment can install the project and run `booksys --help`.
- [x] 1.5 Create the private `booksys` package partitions for operations, domain, packages, learning, storage, projections, migration, and installation without exposing internal imports; verify an architecture test permits only the documented public entry points.

## 2. Root Configuration and Domain Contracts

- [x] 2.1 Define the root configuration schema and resolution order for command overrides, configured `system_root`/`data_root`, and the project-local compatibility default; verify unit tests cover each precedence case and invalid configuration fails closed.
- [x] 2.2 Implement safe root resolution and write-policy checks that constrain private data, staging, projections, and operations to `data_root`; verify traversal, alias, and incompatible-root tests fail without writes.
- [x] 2.3 Define versioned schemas and typed contracts for book, chapter, concept, relation, claim, aliases, evidence classes, and resource roles; verify schema fixtures cover duplicate names while preserving distinct immutable IDs.
- [x] 2.4 Define versioned operation request, result, snapshot, diagnostic, revision, and receipt contracts; verify all schemas reject unknown or malformed protocol fields and accept canonical fixtures.
- [x] 2.5 Define package-manifest and provenance contracts including resource role, media type, byte size, SHA-256, generator metadata, raw digest, and character spans; verify boundary, digest-mismatch, and unsupported-claim tests.

## 3. Strict Diagnostics and Package Storage

- [x] 3.1 Implement read-only configuration and filesystem diagnostics for `booksys doctor --strict`; verify a before/after filesystem snapshot proves the command makes no changes.
- [x] 3.2 Implement canonical JSON/JSONL readers and writers with stable encoding, ordering rules, schema dispatch, and explicit legacy mode; verify byte-stable round trips and rejection of partial or malformed input.
- [x] 3.3 Implement package-manifest loading and integrity validation for required roles, sizes, digests, identities, references, and indexed chapter completeness; verify every strict-validation scenario in `knowledge-packages` has a passing test.
- [x] 3.4 Implement stable selector resolution by immutable ID, slug, and alias with structured ambiguity diagnostics; verify duplicate display names never silently select or merge an entity.
- [x] 3.5 Implement raw-source span verification and evidence-class validation; verify changed source bytes, out-of-range spans, and unclassified unsupported claims block a commit.

## 4. Deterministic Projections

- [x] 4.1 Implement deterministic renderers for the book registry, concept indexes, glossary, and legacy-compatible package views; verify deleting them and rebuilding produces byte-identical outputs.
- [x] 4.2 Implement deterministic renderers for reading plans/preparation views, review logs, mastery maps, due queues, and calibration alerts; verify replay at a fixed effective time produces byte-identical outputs.
- [x] 4.3 Implement `booksys project --check` as a read-only drift detector and `booksys project --write` as the explicit projection repair path; verify check never writes and write changes only declared generated resources.
- [x] 4.4 Add renderer/version metadata outside user-authored narrative regions and preserve authoritative Markdown reference and chapter-guide content; verify projection rebuilds do not alter narrative bytes.

## 5. Append-only Learning and FSRS

- [x] 5.1 Define versioned reading and review event envelopes with stable aggregate IDs, timezone-aware timestamps, payload versions, idempotency keys, and supersession references; verify schema and correction-chain tests.
- [x] 5.2 Implement event append, replay, checkpoint validation, and duplicate/conflicting idempotency handling; verify identical retries are no-ops and conflicting reuse fails without changing the log.
- [x] 5.3 Implement reading-state and mastery reducers while enforcing that coach writes only reading events and trainer writes only review events; verify cross-stream write attempts fail.
- [x] 5.4 Implement the private FSRS adapter with pinned library/version metadata and desired retention default `0.90`; verify published scheduling goldens and explicit failure when the dependency is missing or incompatible.
- [x] 5.5 Implement review evidence capture for EMT expectations, misconceptions, hits, score, objective result, confidence, user pre-feedback rating, final rating, and scheduler policy; verify objective failure forces Again while objective pass preserves the user's rating.
- [x] 5.6 Implement legacy schedule preservation and per-concept takeover on the next observed review without synthesizing historical ratings; verify migrated due queues remain unchanged before review and switch reproducibly to FSRS afterward.

## 6. Operation Workspace and Transactional Commit

- [x] 6.1 Implement concrete `prepare` handlers for reader extraction/finalization, user analysis, coach preview/completion, and trainer quiz/report; verify each workspace contains only its required context and protocol files.
- [x] 6.2 Implement operation workspace lifecycle under `data_root`, including normalized request, minimal context, instructions, result schema, input snapshot, expiry, and safe cleanup; verify cleanup cannot remove committed receipts or paths outside the workspace root.
- [x] 6.3 Implement commit validation for prepared origin, result schema, stable references, provenance, domain rules, and stale snapshots; verify every failure leaves authoritative files and projections unchanged.
- [x] 6.4 Implement the local single-writer lock, recoverable journal/staging, durable event append, projection staging, and atomic logical revision swap; verify injected failures at each phase recover to either the old or complete new revision.
- [x] 6.5 Implement commit receipts and operation-level idempotency so an identical retry returns the prior receipt and conflicting content fails; verify receipts list revision, resources, projection state, and diagnostics.
- [x] 6.6 Add public-interface integration tests that execute representative prepare/result/commit workflows in temporary `data_root` instances without importing private handlers; verify all four skill workflows pass.

## 7. Legacy Migration and Compatibility

- [x] 7.1 Implement deterministic legacy ID assignment with a persisted mapping for every existing book, chapter, concept, relation, and learning aggregate; verify repeated migration plans assign identical IDs.
- [x] 7.2 Implement `booksys migrate plan` to report mappings, unresolved references, missing provenance, projection differences, schedule treatment, and a deterministic plan digest without writes; verify a filesystem snapshot remains unchanged.
- [x] 7.3 Implement staged import of v1 Markdown/package data into manifests, structured facts, retained narrative Markdown, and source provenance; verify both books and all 31 chapters pass strict staged validation.
- [x] 7.4 Implement import of reading/mastery history and legacy due state without inventing Hard/Good/Easy ratings; verify event counts, observable mastery, and due dates match the recorded baseline.
- [x] 7.5 Implement semantic and scheduling parity reports plus atomic migration cutover and rollback metadata; verify a full fixture migration can cut over and restore the exact v1 pointer/state.
- [x] 7.6 Convert all supported legacy pipeline entry points into thin `booksys` adapters with deprecation diagnostics and no independent write logic; verify characterization tests and a static/business-logic boundary check pass.

## 8. Self-contained Skills and Installation

- [x] 8.1 Rewrite the four canonical skill bundles so each owns its referenced guidance/assets and delegates concrete workflows to `booksys`; verify every relative reference resolves when the bundle is copied outside the repository.
- [x] 8.2 Remove storage paths, projection ordering, scheduler mechanics, and duplicated policy from skill instructions while retaining trigger boundaries and semantic responsibilities; verify instruction lint and behavioral evals pass.
- [x] 8.3 Implement per-skill project/user-scope installation for `.agents/skills` and `.workbuddy/skills`, using verified Windows junctions, supported-platform symlinks, and explicit-only copying; verify platform-specific installer tests.
- [x] 8.4 Implement managed-link receipts, current/stale detection, and collision-safe updates that never replace unrelated real directories or sibling skills; verify existing OpenSpec skill fixtures remain byte-for-byte untouched.
- [x] 8.5 Implement `booksys skills doctor` for bundle digest, target, link type, stale state, and supported-harness diagnostics; verify unsupported targets produce guidance and no guessed paths.
- [x] 8.6 Build a sanitized default distribution containing code, schemas, templates, skill bundles, and fixtures while excluding raw texts, formal user books, learning events/projections, machine anchors, and operation workspaces; verify the release manifest and a denylist scan.

## 9. Full Verification and Cutover

- [x] 9.1 Run the complete unit, schema, property, interface-integration, fault-recovery, scheduler, projection, installer, and migration suites from a clean environment; verify every suite passes with no hard-coded historical test count.
- [x] 9.2 Run candidate-versus-baseline behavioral evals for all four skills; verify zero fabrication, spoiler leakage, unauthorized writes, premature quiz feedback, mutable EMT expectations, or unsupported claims, and publish the soft-metric comparison.
- [x] 9.3 Execute migration planning and staged apply for the real two-book, 31-chapter dataset, resolve every ambiguity, and record reviewed parity and plan-digest evidence; verify strict doctor passes on staging before cutover.
- [x] 9.4 Atomically cut over the real data pointer and install the validated four skills into `.agents` and `.workbuddy` while retaining v1 data and adapters; verify end-to-end smoke workflows, link receipts, and rollback readiness.
- [x] 9.5 Document the compatibility-cycle start, rollback/reconciliation procedure, deprecation telemetry, operator commands, root configuration, and private-data boundaries; verify a fresh-user walkthrough can install, diagnose, migrate, and run one workflow using only the documentation.
- [x] 9.6 Remove Python bytecode caches, duplicated sample fixtures, and obsolete generated core artifacts only after their replacements are verified; verify strict doctor, release denylist, and the full test/eval suite still pass, while deferring compatibility-adapter removal to a later OpenSpec change.
