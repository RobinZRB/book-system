## Context

The current `user.analyze` operation only normalizes the optional
`external_facts` request field.  Research may happen in the conversation, but
there is no contract that returns its results to the prepared manifest. See
`proposal.md` for motivation.

## Goals / Non-Goals

**Goals:**

- Give synthesis one structured, provenance-preserving fact package containing
  positive facts, counter-evidence, conflicts, and missing fields.
- Keep `booksys` deterministic and read-only by treating research as an input
  boundary rather than embedding browser/network behavior in preparation.
- Make parallel research roles useful without allowing them to create
  unsupported conclusions or mutate knowledge packages.

**Non-Goals:**

- Persist a market-data warehouse, provide trading signals, or guarantee that
  real-time market data is available.
- Let a research role modify books, learning state, operation results, or the
  final conclusion directly.

## Decisions

### Separate research orchestration from deterministic preparation

The book-user workflow will first prepare book context, then derive a visible
research plan from its selected protocol, Gate, red flags, dimensions, and
evidence gaps. It invokes independent research and counter-evidence roles only
for plan fields when an external research capability is available. Their
outputs are normalized into a fact package and passed to a fresh `user.analyze`
preparation call for synthesis. `booksys` validates and reports the input
package; it does not browse itself.

Embedding browsing in `booksys` was rejected because it would make a formerly
deterministic, fast operation dependent on credentials, source availability,
and non-repeatable web state.

### Make every research field traceable to the framework

The research plan records each requested field, its linked framework item,
whether it addresses supporting evidence or counter-evidence, source-tier
preference, and applicable date. The final answer can therefore show why a
fact was sought, not merely where it was found. Research agents may report an
additional risk only when it is linked back to a protocol dimension or red
flag before synthesis.

The alternative—giving research agents a broad company-research prompt—was
rejected because it spends time on unneeded facts and makes the evidence chain
hard to audit.

### Use a small canonical fact schema and source tiers

Every fact will require a subject, field, value, source identity, retrieved
time, applicable date, source tier, and status.  Source tiers are: primary
(issuer/exchange/regulator), secondary (established reporting or data vendor),
and unverified caller claim. The package will retain, not collapse, duplicate
or conflicting facts for a field/date.

The alternative of free-form research notes was rejected because a synthesizer
cannot reliably distinguish a source citation from an analyst inference.

### Use independent positive and counter-evidence roles

The fact-research role gathers current financial/market facts; the
counter-evidence role searches for material risks, adverse disclosures, and
contradictory facts. Both deliver facts only. A synthesizer is the sole role
allowed to apply the book framework and must state the searched scope when no
counter-evidence is found.

The alternative of one general research role was rejected because it couples
the supporting narrative and challenge narrative, increasing confirmation bias.

### Preserve caller-supplied and offline paths

Callers can supply an already-valid package. If no research capability exists,
the workflow emits an offline diagnostic and proceeds with the available book
evidence; it never labels missing data as a pass.

## Risks / Trade-offs

- [Agent research sources vary in quality] → enforce source tiers and require
  primary sources for financial facts where available.
- [Different roles find incompatible figures] → retain conflicts and block an
  uncontested synthesis claim.
- [Parallel work raises response latency] → run research roles concurrently
  and keep book-context preparation local and fast.
- [Research is unavailable in some harnesses] → preserve caller-supplied and
  offline fallback paths.

## Migration Plan

1. Introduce the framework-driven research plan and canonical fact package
   while accepting the existing `external_facts` list as a compatibility input.
2. Update book-user orchestration and guidance to build the plan, perform
   plan-scoped research, and reinject the package.
3. Add deterministic fixtures for plan coverage, primary, missing, stale,
   conflicting, and counter-evidence cases; then enable detailed synthesis
   from the package.

Rollback disables orchestration and retains the caller-supplied external-facts
path; no authoritative book or learner data is changed.
