## Why

Learning history is append-only, but review writes currently check only that required payload keys exist and `doctor` checks only a small event-envelope subset. Malformed values can therefore enter the authoritative stream or remain undetected until a derived-state command fails, making the recorded learning state unreliable.

## What Changes

- Validate reading and review write inputs against domain invariants before an event is appended.
- Validate complete event envelopes and kind-specific payloads when reading the event stream.
- Make `learn status` and `learn due` fail explicitly on an invalid authoritative event instead of producing partial or misleading derived state.
- Extend `doctor` with line-specific, read-only diagnostics for malformed or internally inconsistent learning events.
- Add regression coverage for invalid writes, corrupt historical events, valid FSRS event replay, and in-process CLI command behaviour.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `learning-state`: learning commands enforce typed review and event invariants, and derived state rejects corrupt authoritative history.
- `booksys-operations`: `doctor` reports line-specific learning-event invariant failures without altering the stream.

## Impact

- Affected code: `src/booksys/learning/`, `src/booksys/cli.py`, and learning/CLI tests.
- API behaviour: invalid review submissions and corrupt historical event streams now return actionable errors rather than being accepted or partially processed; valid learning commands keep their existing behaviour.
- Storage format: no migration, rewrite, automatic repair, or new runtime dependency; existing valid schema-version-1 events remain supported.
