## Context

See [proposal.md](proposal.md). `prepare()` currently creates the same generic workspace for every intent. For `user.analyze`, it copies an absent `book-user/README.md`, supplies no selected protocol or evidence, and writes instructions that contradict its read-only flag. The existing book-user data already contains the inputs needed for deterministic selection: the book registry, a book profile with keyword-to-chapter mappings, chapter concept indexes, and protocol templates.

## Goals / Non-Goals

**Goals:**

- Make `user.analyze` a useful v2 read interface whose output alone is sufficient for the book-user skill to begin an evidence-backed analysis.
- Preserve deterministic preparation while making coverage and failures inspectable; do not impose a default context-size ceiling.
- Make analysis quality and performance regressions testable before the path becomes the default.

**Non-Goals:**

- Fetching market, company, or regulatory data from a provider.
- Generating or persisting the natural-language investment answer.
- Reintroducing the legacy workflow as a runtime fallback.
- Replacing book-package formats or rebuilding book content in this change.

## Decisions

### 1. Give `user.analyze` a typed request and a read-only result manifest

The request will accept a query, an optional exact book selector, an optional category scope, optional external facts, and an explicit `search_scope` (`indexed` by default; `whole_book` only after the caller chooses it). It will return the usual operation identity/path plus an analysis manifest stored in the read-only workspace.

The manifest will carry a stable status (`ready`, `insufficient_evidence`, `ambiguous`, or invalid-request failure), selected books/protocols, evidence references and excerpts, protocol-section execution records, external-fact records, and an audit summary. The workspace will contain a read-only `instructions.md` describing how to consume it, never a `result.json` instruction or schema.

Keeping the response manifest in the workspace preserves the v2 operation interface and lets callers inspect the exact context used. Returning only stdout was rejected because it makes the assembled prompt and diagnostics hard to audit.

### 2. Use two-stage deterministic evidence selection

Stage one reads only the registry, selected profiles, glossary/concepts indexes, and protocol metadata. It normalizes query tokens and maps every keyword/profile/concept match to protocol sections; it does not calculate relevance scores or discard lower-ranked matches. Stage two reads `reference.md`, `concepts.md`, and `relations.md` for every matched candidate. There is no default excerpt or context-size limit; an optional caller-supplied budget may truncate payload files while preserving every matched record and its source path in the manifest.

The selector records every matched candidate and the keyword(s) that caused the match. It reserves space for the profile, protocol, and report before consuming evidence so that an analysis never loses its operating contract to long chapter text. Semantic/vector search is deliberately excluded: the project has curated, deterministic indexes and a strict 300ms budget; a future change can add a separately evaluated semantic selector.

### 3. Treat insufficient coverage as a first-class result

The selector will calculate coverage against the applicable protocol sections rather than only counting keyword matches. It returns `insufficient_evidence` when a required section lacks usable book evidence. Matched sections remain analyzable; missing sections are explicitly marked unassessed. It does not automatically read the whole book.

An explicit `whole_book` follow-up repeats selection against all chapters with its own larger documented budget and reports that it expanded scope. This preserves the user's choice between diagnosing the index/selector and accepting a more expensive search.

### 4. Keep book evidence, external facts, and missing fields separate

Book evidence records will contain book/chapter/resource identity, excerpt, evidence type, and citation label. External facts will be accepted as caller input and preserve `source`, `retrieved_at`, `applicable_at`, `field`, and `value`; absent values are recorded as missing/unverified rather than discarded. The preparation layer does not fetch or infer external facts.

This separation avoids treating a current company claim as a statement from a book, and lets the final response expose unavailable data without fabricating a conclusion.

### 5. Make bundle guidance small but operational

`skills/book-user/resources/guidance.md` will instruct the skill to call the typed preparation request and consume its manifest, then run every applicable protocol section with its reported evidence status. The skill will show a compact trace summary by default and expand the full audit when coverage is insufficient, external facts are missing, or the user requests audit detail.

The old standalone usage guide remains data/documentation during the migration but is not a runtime fallback. The canonical behavior lives in the v2 manifest and bundle guidance.

### 6. Gate the path with deterministic and behavioral tests

Fixtures will encode stock-analysis requests, expected book/protocol selection, required chapter hits, expected misses, ambiguity, incomplete external facts, and explicit whole-book expansion. Unit tests lock down scoring, ordering, caps, and diagnostic output. Integration tests exercise the public CLI and verify a read-only workspace has no writable result contract. Performance tests use local fixtures and a conservative warm-run budget of 300ms; behavioral evals inspect protocol-section status and citation-capable evidence rather than judging prose length.

## Risks / Trade-offs

- [Curated indexes omit relevant wording] → Return `insufficient_evidence` with matched triggers and missing sections; require explicit whole-book search rather than silently masking the gap.
- [A mandatory investment protocol has many sections] → Report every section's attempted/matched state, prioritize protocol-required evidence, and report budget exhaustion instead of claiming coverage.
- [Markdown evidence is too large for the budget] → Apply deterministic excerpt limits with resource identity and retain the complete source path for on-demand inspection.
- [Caller supplies stale or partial external data] → Preserve timestamps and missing fields as unverified; do not merge them into book evidence.
- [Performance differs across machines] → Test a fixed local fixture with a budget and report timing; do not make latency a correctness claim about external retrieval.

## Migration Plan

1. Add the new manifest and selector behind `user.analyze` while retaining the existing public intent name.
2. Add fixtures and tests; run the fixed evaluation suite in validation mode.
3. Replace the placeholder book-user guidance with manifest-consumption guidance once all gates pass.
4. Roll back by restoring the former generic preparation handler and bundle guidance; no authoritative book or learner data is changed by this feature.

## Open Questions

None.
