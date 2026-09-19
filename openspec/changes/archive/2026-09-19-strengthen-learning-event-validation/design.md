## Context

See [proposal.md](proposal.md). The current service verifies only review payload key presence before constructing an event, while `doctor` verifies only a few envelope fields. `status` and `due` replay raw JSONL directly, so malformed historical data can yield an exception late in a projection or a partial result.

## Goals / Non-Goals

**Goals:**

- Make one shared validation contract enforceable before writes and during event-stream replay.
- Preserve valid version-1 event compatibility without changing, rewriting, or repairing stored bytes.
- Give `doctor` enough source location to report independent failures per event line.
- Ensure derived-state commands do not silently continue after authoritative history is invalid.

**Non-Goals:**

- Recompute or cryptographically verify historical FSRS schedules.
- Add schema-validation dependencies, event migrations, automatic repair, or a new persistent projection.
- Change idempotency semantics or the published knowledge-package format.

## Decisions

### Centralize domain validation in the learning package

A shared validator will validate review submissions, event envelopes, reading payloads, review payloads, and recorded schedule shapes. Service writes and event replay will call the same rules, preventing drift between accepted writes and health checks.

Alternatives considered:

- Validate only in CLI: rejected because service APIs and tests can bypass the CLI.
- Use the JSON Schema document at runtime: rejected because the project currently treats schemas as reference documentation and needs cross-field domain checks that are clearer in dependency-free Python.

### Fail closed for derived state

`status` and `due` will reject an invalid authoritative event rather than skip it. A partial projection could present an incorrect mastery or due result without making the damaged history visible.

Alternatives considered:

- Skip invalid events and return warnings: rejected because the caller could mistake incomplete state for valid state.
- Repair or rewrite invalid events: rejected because event history is append-only.

### Diagnose events line by line

Event iteration will retain JSONL line numbers for validation callers. `doctor` will continue after a validly parsed but invalid event so it can report all such violations; unrecoverable JSON syntax errors will report their line and end further parsing only when later records cannot be read safely.

Alternatives considered:

- Report only the file: rejected because users cannot safely identify an event to correct by appending a compensating event.

### Validate schedule structure, not recomputed schedule equality

Validation will require a timezone-aware due timestamp, matching final rating, valid FSRS state values and field types, plus scheduling and parameter version strings. It will not recompute the exact FSRS result, because stored events can legitimately have a recorded scheduler version or policy that differs from the current runtime.

### Test the CLI in process

CLI integration tests will invoke the public CLI entry point with explicit arguments and isolated temporary project/data roots, then capture JSON output, stderr, and return codes. This exercises argument dispatch and error rendering without spawning a shell or depending on the Windows batch launcher. The launcher remains outside this validation change's test scope.

## Risks / Trade-offs

- [Valid but previously unconstrained historical events fail after upgrade] → retain version-1-compatible rules for emitted events and expose exact `doctor` diagnostics rather than modifying data.
- [Strict replay blocks a user with one damaged line] → provide line-specific diagnostics; correction remains append-only and manual by design.
- [Validation rules grow separately from the public schema] → add regression tests for both generated events and corrupt fixtures, and keep schema changes limited to contract-level changes when needed.
- [CLI tests accidentally depend on workspace state] → every CLI case supplies temporary roots and asserts only command output, exit status, and the fixture event file.

## Migration Plan

1. Release validation alongside `doctor` diagnostics; no event bytes change.
2. Operators run `doctor` before relying on derived state after upgrade.
3. For an invalid historical record, retain the original bytes and append a corrective event only when the domain supports that correction; no automatic migration or deletion occurs.
4. Rollback is code-only: the event format remains version 1 and no data conversion is performed.
