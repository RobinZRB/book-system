## Why

`user.analyze` can preserve caller-supplied external facts but does not acquire
or merge them.  Stock analysis therefore has a reliable book framework yet
reports missing price, financial, and counter-evidence fields even when an
agent separately researched them during the same answer.

## What Changes

- Add a read-only, book-framework-driven external-fact research stage for
  investment/company analysis that produces only the citation-ready facts the
  selected protocol, Gate, red flags, and dimensions require before synthesis.
- Define source tiers, field-level provenance, freshness, conflict, and
  missing-data rules; official issuer, exchange, and regulator disclosures are
  preferred for financial facts.
- Add an orchestration contract that derives a research plan from selected book
  evidence, then dispatches independent fact and counter-evidence research.
  The synthesis role merges only validated, plan-linked facts into the
  `user.analyze` request and keeps book evidence separate.
- Preserve a no-network/offline fallback: callers can supply facts directly,
  and an unavailable research capability is disclosed rather than fabricated.

## Capabilities

### New Capabilities

- `external-fact-research`: Structured, provenance-preserving acquisition and
  validation of current investment-analysis facts and counter-evidence.

### Modified Capabilities

- `booksys-operations`: Analysis preparation must accept a validated external
  fact package and expose its completeness, conflicts, and freshness in the
  read-only manifest.
- `skill-distribution`: The book-user bundle must orchestrate research and
  synthesis roles, use the offline fallback safely, and evaluate provenance
  and counter-evidence behavior.

## Impact

- Affects book-user instructions, `user.analyze` request/manifest validation,
  tests, and behavioral evaluations.
- Requires an agent-accessible research capability at runtime, but introduces
  no persistent market-data store and does not modify books or learner data.
