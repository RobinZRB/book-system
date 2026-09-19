## Context

`user.analyze` currently produces a manifest containing selected books,
protocol headings, evidence files, and diagnostics.  The manifest records only
coarse `matched`/`unmatched` states, while the bundle guidance requests a
normally concise answer.  See `proposal.md` for motivation.

## Goals / Non-Goals

**Goals:**

- Make detailed investment analysis the default presentation from the existing
  prepared evidence bundle.
- Produce deterministic execution records for Gate checks, risks, dimensions,
  counter-evidence, and missing external facts.
- Preserve fast indexed preparation, all-match retrieval, read-only behavior,
  explicit whole-book expansion, and partial analysis.

**Non-Goals:**

- Fetch market data, calculate investment scores, make a buy/sell decision, or
  impose an evidence cap.
- Recreate the legacy placeholder protocol or change book-package facts.

## Decisions

### Add an analysis-plan object to the manifest

Preparation will derive a compact `analysis_plan` from the selected protocol,
profile keyword map, and evidence inventory.  It will record the presentation
mode, Gate checks, red-flag candidates and disposition states, dimensions, and
counter-evidence status.  This makes the user-visible sequence testable and
keeps the AI from having to infer structure from protocol prose.

The alternative—placing a fixed outline solely in guidance—would not be able
to distinguish an unmatched section from an unexecuted one, and would weaken
traceability.

### Preserve explicit states instead of automatic pass/fail judgments

Each Gate, risk, and dimension will use stable states such as `matched`,
`unmatched`, `unassessed`, `not_triggered`, `investigate`, and `external_facts_missing`.
The AI will turn evidence into a conclusion, but cannot silently upgrade an
unknown condition to pass.  The plan will also identify whether a counter-view
was found in the selected scope.

The alternative of a numeric quality score is rejected because the user has
already requested all matched evidence to remain visible without score-based
elimination.

### Make presentation mode request-aware

Investment/finance category requests default to `detailed`; an explicit brief
request selects `concise`.  Other categories retain concise behavior.  The
guidance will define exact headings and disclosure requirements for detailed
mode, with a compact equivalent for concise mode.

The alternative of making every request detailed would add unnecessary latency
and output burden to ordinary conceptual questions.

### Test the manifest contract and rendered behavior separately

Unit/integration tests will assert deterministic analysis-plan construction and
partial-evidence states.  Behavioral evaluation fixtures will assert that the
book-user output instructions require all detailed sections and no unsupported
claims.  This catches both runtime regressions and prompt/bundle regressions.

## Risks / Trade-offs

- [Protocol headings do not encode a clean risk/dimension taxonomy] → use a
  documented deterministic mapping with conservative `unassessed` fallback.
- [More metadata could affect the preparation target] → store compact records,
  retain no default context cap, and extend the warm-run regression measurement.
- [Detailed output can feel repetitive] → honor explicit concise requests while
  preserving the minimum audit disclosures.
- [External facts may be absent] → surface field-level gaps and prohibit a
  passing verdict based on their absence.

## Migration Plan

1. Add the manifest plan alongside existing fields, retaining existing fields
   for compatibility.
2. Update bundled guidance to consume the new plan, falling back to visible
   unmatched disclosures for older workspaces.
3. Add tests and evaluations, run the health and regression suites, then make
   the plan the documented default for investment requests.

Rollback consists of reverting the guidance to concise presentation; manifests
remain read-only operation artifacts and do not mutate package data.
