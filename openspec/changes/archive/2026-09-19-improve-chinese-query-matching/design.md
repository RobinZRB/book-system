## Context

See [proposal.md](proposal.md). `analysis_context.py` hardcodes a 16-word investment keyword set for category selection and tokenizes queries into a full run plus overlapping bigrams. Measured against the active catalog, five representative Chinese queries — including two naming a book's own core keyword — select zero books and raise `insufficient_evidence` with no candidates. Yet the `user.analyze` request already supports explicit `book`/`category` selectors, and the selected book's profile (chapter index plus keyword map) is already written into the prepared context. The missing pieces are small and specific: failures return nothing to choose from, and chapters cannot be named explicitly.

An earlier draft of this change proposed a catalog-driven lexicon, a precomputed index projection, IDF-weighted scoring, and scale fixtures. It was rejected in review as over-engineered: the caller of this selection is itself an AI that performs synonym recognition, semantic book choice, and ambiguity judgment natively. Building deterministic machinery to imitate that judgment duplicates the caller's competence and adds permanent maintenance surface (data files, schemas, projections, fixtures) for a two-book catalog. The correct division of labor: the runtime does what must be recomputable (catalog exposure, evidence assembly, provenance, budgets); the AI does what requires understanding (choosing books and chapters); and every AI decision returns as a structured selector so preparation stays exactly replayable. Determinism here means "an AI decision, once made, is replayed identically" — not "the machine decides instead of the AI".

## Goals / Non-Goals

**Goals:**

- No bare selection errors: every automatic-selection failure returns a structured, compact catalog the caller can act on.
- Caller-driven chapter selection: the skill can name exact chapters after reading the selected book's profile.
- Match reasons that name real dictionary keywords, not bigram fragments.
- A book-user workflow that makes the AI's selection step explicit, recorded, and auditable.
- Scale by tiering (compact list → profile on demand), not by new indexing machinery.

**Non-Goals:**

- No runtime lexicon/synonym database, no scoring or ranking, no catalog-index projection, no new schemas or data files, no new dependencies.
- No semantic/embedding selector (deferred indefinitely; reconsider only on measured behavioral-eval failure).
- No change to book-reader, package formats, protocols, evidence assembly, or the external-fact contract.
- No relevance ranking or eviction within a selected book's chapter evidence (existing no-ranking contract stays).

## Decisions

### 1. Selection failure returns a tiered catalog, never a bare error

When the exact selector and the convenience keyword matching both fail to select any book, preparation returns status `insufficient_evidence` with `candidates`: a compact per-book summary — slug, title, category, aliases, profile path, and chapter directory names. Keyword maps, profile bodies, and chapter internals are deliberately excluded; they arrive with the profile once a book is chosen. This two-tier disclosure keeps the candidate payload bounded by catalog size rather than by book size (measured on the active catalog: 1840 bytes for two books, ~920 bytes per book, of which the chapter directory names are the bulk at 10 and 21 entries), and it respects the existing optional context budget: when a budget is supplied, chapter lists are shortened first and books are never dropped, so a caller always sees the whole catalog.

The current convenience keyword matching (including the 16-word category set) is kept unchanged: it is a best-effort default that works for queries already containing domain words, and its failures now degrade gracefully instead of erroring. Deleting it would make today's passing fixtures meaningless; leaving it costs nothing once the failure path is fixed.

### 2. Explicit chapter selection in the request

The `user.analyze` request gains an optional `chapters` array of chapter directory names (or unique prefixes). Named chapters are validated against the selected package; unknown names fail with the available chapter list. Valid names become the chapter candidates with reason `caller_selected`, bypassing keyword matching. `whole_book` remains the explicit all-chapters mode; `chapters` is the surgical mode the skill uses after reading the chosen book's chapter index and keyword map — whose complete presence in the prepared context Decision 4 guarantees.

### 3. Bidirectional keyword matching and honest match reasons

Chapter keyword matching becomes symmetric: a hit occurs when a query token appears inside the keyword cell (current behavior) or when the full keyword text appears in the query. Match reasons record the keyword-cell text, not the query fragment.

Measured behavior of the current code matters for scoping this correctly. Recall is already largely intact: because the tokenizer emits overlapping bigrams, 用安全边际的思路看平安 already matches the 安全边际 keyword row's chapters (Ch20, Ch11, Ch13) — through the bigram 安全 rather than the keyword. The real defect is the reason label, which reads `keyword:安全,全边,边际`: it names garbage fragments and omits the dictionary term that actually governs the mapping. So this decision is primarily a provenance fix, not a recall fix; the bidirectional check closes the residual case where a multi-character keyword has no overlapping bigram inside a longer run, and makes the reason legible for audit.

The synonym gap is deliberately left to the caller: 看看PE和净资产 currently reaches only chapters mapped to 资产, because PE and 市盈率 are not related anywhere in the runtime. The calling AI knows this equivalence natively and is expected to name chapters explicitly when its query uses a synonym — which is exactly what Decision 2 exists for. Encoding a synonym table in the runtime would reintroduce the maintenance surface this change removes.

### 4. The AI owns selection; the runtime records it

book-user guidance becomes a two-phase workflow. Phase one: prepare with the raw query (plus any selector the user supplied). If the result is `ready`, proceed. If candidates arrive, the skill chooses book(s) — asking the user when the choice is genuinely ambiguous — and retries with an explicit `book` selector. Phase two: the skill reviews the chosen book's chapter index and keyword map, judges whether the default chapter candidates cover the question, and retries with explicit `chapters` when they do not. Each retry records a `selection_rationale` string in the request, which preparation copies into the manifest and operation receipt. The audit trail therefore preserves the full decision chain: what was offered, what was chosen, by whom, and why — replayable byte-for-byte, because final context depends only on recorded structured inputs.

Phase two depends on the profile's two governing tables being readable, and this change must guarantee it. Preparation currently writes only the first 2200 characters of the profile into the context: measured against the active catalog, the keyword-to-chapter map starts at character 4242 (聪明的投资者) and 2776 (Serenity的瓶颈点投资方法论), so it is always truncated, and only 9 of 21 (respectively 8 of 10) chapter-index rows survive. Preparation will therefore include the complete chapter index and keyword-to-chapter map as dedicated context sections (bounded by their real size, typically a few KB) and continue to record the profile's full path, so the skill can also read the source file directly. Without this, phase two would be guesswork.

### 5. Distinguish why selection produced no analysis

`insufficient_evidence` currently covers only one meaning — the book was chosen but some protocol sections had no matched evidence. Adding candidates introduces a second, different meaning — no book was chosen at all. Preparation will carry an explicit diagnostic (for example `selection_failed` plus a candidate count) so a caller can tell "pick a book and retry" apart from "the book has no evidence for these sections, consider whole-book search" without inferring it from an empty `books` array.

### 6. Scale without machinery

Catalog growth is absorbed by the tiered disclosure in Decision 1 and by the profile-on-demand flow that already exists. Measured on the active catalog: 1840 bytes total, 920 bytes per book with chapter names and 340 bytes per book without them (~37 bytes per chapter-name entry), so a 200-book catalog projects to ~180 KB with names or ~67 KB without. The former is still plainly readable by a caller, and the chapter names are what make phase two possible without a second fetch (Decision 4 / Open Question 1). If a catalog ever makes the full list unwieldy, the answer is paging or category-filtering the list — small additive changes — not a scoring engine. Synthetic large-catalog fixtures are unnecessary because no new scale-sensitive machinery is introduced; existing performance tests continue to guard the 300ms budget, and the measured failure path costs 18ms while a full three-round query → book → chapters flow costs 34ms wall.

## Risks / Trade-offs

- [Caller picks the wrong book] → The choice is explicit, recorded with rationale, and visible in the manifest; behavioral evals include fixtures where the correct book must be chosen from candidates. This risk exists with any selector and is cheaper to inspect than a scoring engine's threshold.
- [Extra prepare round-trips] → Worst case is query → candidates → book → chapters: three warm prepares at ~300ms each plus the skill's own latency. Acceptable for an analysis workflow; the common case (domain word present, or caller passes a selector upfront) stays at one pass.
- [Convenience matcher kept means some queries still auto-select the obvious shelf] → Intended. It is a default, not an authority; candidates remain available whenever it fails, and explicit selectors always override it.
- [Candidates list grows long] → Compact per-book entries only; chapter internals excluded; category filter can be added later as a small change if the list ever becomes unwieldy.
- [Bidirectional matching over-matches short keywords] → Keyword-map cells are curated multi-character terms; the keyword-map table remains the authority for what can trigger a chapter, unchanged by this fix.
- [Profile excerpt truncation silently starves phase two] → Addressed in Decision 4 by writing the chapter index and keyword map as dedicated context sections; a fixture asserts both tables are complete in the prepared context for the active catalog.
- [Chapter 导言 (00-本书的目的) is unreachable through the keyword map] → Verified: keyword rows mention 导言, but the chapter resolver parses only `Ch<digits>` tokens, so a keyword mapped to 导言 never yields chapter 00. Explicit `chapters` selection covers it (and Ch0 becomes nameable for the first time); extending the resolver to map 导言 is optional and out of scope unless the skill proves unable to compensate.
- [Synonym queries such as PE/市盈率 reach fewer chapters by default] → Intentional: the caller knows the equivalence and uses explicit `chapters`; the runtime stays free of synonym data. Behavioral evals record whether this compensation actually happens.

## Known residual gaps (disclosed, deliberately not fixed here)

- Book auto-selection still cannot resolve a bare company-name query by itself. The AI round-trip (candidates → explicit `book`) is the designed mechanism, so a non-AI CLI caller must choose from candidates manually.
- Only the current catalog's behaviour was measured. The tiered candidates payload is argued to scale (compact entries, profile on demand) but is not proven at hundreds of books; no synthetic scale fixture is introduced, precisely because no new scale-sensitive machinery is added.

## Migration Plan

1. Add the candidates-on-failure path, the catalog-summary builder, and the selection-failure diagnostic with unit fixtures for the five reproduced queries.
2. Add the `chapters` request field with validation and `caller_selected` reasons, plus the complete chapter-index and keyword-map context sections; add fixtures for explicit and mixed selection.
3. Apply the bidirectional match fix and reason relabeling; verify existing fixtures still pass.
4. Update book-user guidance with the two-phase workflow and rationale recording; extend behavioral eval gates.
5. Roll back by restoring the former selection failure path and dropping the `chapters` field; no authoritative data is touched by this change.

## Open Questions

- Exact candidates payload budget: include chapter directory names always (useful for phase two) or only under a size threshold? **Resolved in implementation:** always include, and when the caller supplies `context_budget_bytes` shorten chapter lists before anything else so no book is ever dropped from the list. Measured cost of always including: ~920 bytes per book on the active catalog.
