## Why

`booksys prepare user.analyze` currently creates an operation directory but does not select a protocol or supply book evidence. Its configured guidance source is absent, and its read-only instructions incorrectly describe a writable result/commit path. This adds orchestration latency while reducing the evidence and protocol coverage that made the prior analysis workflow useful.

## What Changes

- Make `user.analyze` preparation build a deterministic analysis context: selected book(s), protocol, profile, all matched chapter evidence, and a machine-readable execution report. No default context-size ceiling is applied.
- Add two-stage evidence selection: lightweight index/profile matching before loading every matched chapter; do not silently widen to a whole-book search.
- Return actionable insufficient-evidence diagnostics and support an explicit whole-book-search request mode.
- Separate book-derived evidence from optional external facts, recording source, retrieval time, applicable date, and missing fields.
- Correct read-only operation artifacts so they contain no result/commit instructions or writable contract.
- Update the book-user bundle to consume the prepared context and present concise normal summaries with expandable audit detail.
- Add deterministic selection, integration, performance, and behavioral evaluation gates for stock-analysis requests.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `booksys-operations`: strengthen the read-only analysis preparation contract with bounded evidence, diagnostics, explicit expansion, and a non-writable workspace.
- `skill-distribution`: require book-user evaluation coverage for analysis traceability, context budgets, and evidence-quality regressions.

## Impact

- Affected runtime: `src/booksys/operations/workspace.py`, package selection helpers, CLI request handling, and book-user skill guidance.
- Affected tests/evals: core and migration-stage tests plus new deterministic fixtures and behavior/performance gates.
- No new external provider is required; external facts remain caller-supplied or separately acquired optional input with provenance.
