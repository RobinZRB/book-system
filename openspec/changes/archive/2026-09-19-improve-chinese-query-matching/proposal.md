## Why

`booksys prepare user.analyze` selects books with a hardcoded 16-word investment keyword list and selects chapters with full-run-plus-bigram query tokens. Chinese queries that do not literally contain one of those 16 words fail book selection entirely — including queries that directly name a book's own core keyword. Measured against the active two-book catalog, all of the following return zero books: `分析下中国平安`, `看看宁德时代怎么样`, `用安全边际的思路看平安` (安全边际 is a core keyword of 聪明的投资者), `对比下苹果和平安的护城河`, and `分析AXTI的瓶颈点` (瓶颈点 is the Serenity book's title-level keyword). The failure raises `insufficient_evidence` without candidates, so the calling skill cannot recover except by blind retry. The request already accepts explicit `book`/`category` selectors, but there is no way to specify chapters, and no structured catalog is returned for the caller to choose from.

The consumer of selection is an AI skill. Book choice, synonym recognition (市盈率 = PE), and ambiguity judgment are exactly what the caller does well; deterministic evidence assembly, provenance, and budgets are what the runtime does well. The runtime should stop imitating the caller's judgment and instead expose the catalog for it to decide — with every decision returned as a structured selector so the audit trail can replay it exactly.

## What Changes

- On any failure of automatic book selection, return a structured, budget-respecting catalog summary as candidates (per book: slug, title, category, aliases, profile path, chapter directory names) instead of a bare `insufficient_evidence` error. The compact list contains no keyword maps or chapter internals; per-book detail stays in the profile, which is loaded on demand once a book is selected — this tiers disclosure so candidates stay small as the catalog grows.
- Add an optional `chapters` field to the `user.analyze` request: caller-named chapters (validated against the package) become the chapter candidates with reason `caller_selected`, bypassing keyword matching. This lets the calling skill read the selected book's profile (chapter index and keyword map, already in context) and explicitly choose the chapters to load.
- Make chapter keyword matching bidirectional and honest about its reasons: a chapter keyword also matches when its full text appears in the query, and match reasons record the dictionary keyword rather than a bigram fragment. Measured recall is already largely intact (bigrams cover multi-character keywords), so this is primarily a provenance fix — the label `keyword:安全,全边,边际` names garbage and omits the governing term 安全边际. No scoring, no ranking, no lexicon files.
- Guarantee the prepared context actually carries what phase two needs: the selected book's complete chapter index and keyword-to-chapter map become dedicated context sections. Today only the first 2200 characters of the profile are copied, which truncates the keyword map entirely (it starts at character 4242) and most of the chapter index.
- Distinguish the two meanings of `insufficient_evidence` with an explicit diagnostic: "no book selected, choose from candidates" versus "book selected but sections lack evidence, consider whole-book search".
- Keep the existing convenience keyword matching for book/category selection exactly as-is; it remains a best-effort default whose failure now degrades to candidates instead of an error.
- Update book-user guidance to a two-phase workflow: prepare with the query; if candidates are returned, the skill chooses book(s) — asking the user when genuinely ambiguous — and retries with an explicit `book` selector; after reading the profile it may retry with explicit `chapters`. The skill records its selection rationale in the request so the manifest and receipt preserve who chose what and why.
- Extend evaluation gates: the five reproduced failure queries must yield candidates containing the correct books; candidate-based retries must show a recorded selection rationale; no-hit requests must never produce a bare error.

Explicitly rejected after evaluation: a runtime lexicon/synonym database, IDF-weighted scoring, a precomputed catalog-index projection, and synthetic large-catalog fixtures. All four solve problems the calling AI already solves natively, at a maintenance cost the project does not need to carry. A runtime semantic or scoring layer may be revisited only if behavioral evaluations later show the AI-driven workflow failing in practice.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `booksys-operations`: selection failures return structured catalog candidates; `user.analyze` accepts explicit chapter selection; chapter match reasons name dictionary keywords.
- `skill-distribution`: book-user guidance gains the two-phase candidate-driven selection workflow with recorded rationale; evaluation gates cover the reproduced Chinese-query failures.

## Impact

- Affected runtime: `src/booksys/analysis_context.py` (selection failure path, chapter candidate handling, match reasons) and request validation. No new data files, schemas, projections, or dependencies.
- Affected skills: book-user guidance only. book-reader is unchanged.
- Affected tests/evals: new deterministic fixtures for candidates-on-failure, explicit `book`/`chapters` flows, and rationale recording; existing analysis fixtures must keep passing unchanged.
- Preparation remains deterministic, offline, and within the 300ms budget; catalog growth is handled by tiered disclosure (compact list first, profile on demand), not by new indexing machinery.
