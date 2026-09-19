## 1. Candidates on selection failure

- [x] 1.1 Implement the compact catalog-summary builder (per book: slug, title, category, aliases, profile path, chapter directory names) honoring the optional context budget; verify it stays small for the active catalog and contains no keyword maps or chapter internals.
- [x] 1.2 Change the automatic-selection failure path to return `insufficient_evidence` with the structured candidates instead of a bare error; verify the five reproduced queries (分析下中国平安 / 看看宁德时代怎么样 / 用安全边际的思路看平安 / 对比下苹果和平安的护城河 / 分析AXTI的瓶颈点) now yield candidates containing the investment books.

## 2. Explicit chapter selection

- [x] 2.1 Add the optional `chapters` request field with validation against the selected package, unknown names failing with the available chapter list; verify valid names become chapter candidates with reason `caller_selected` and bypass keyword matching.
- [x] 2.2 Verify interplay of `chapters` with `search_scope` (explicit chapters win over indexed matching; `whole_book` unchanged) and that protocol-section states update accordingly.

## 3. Bidirectional matching and match reasons

- [x] 3.1 Make chapter keyword matching symmetric (query token in keyword cell, or full keyword text in query) and record the keyword-cell text as the match reason; verify 用安全边际的思路看平安 matches the 安全边际 keyword row with reason 安全边际 instead of the fragments 安全,全边,边际, and that no existing fixture regresses.

## 3b. Prepared context completeness

- [x] 3.2 Write the selected book's complete chapter index and keyword-to-chapter map as dedicated context sections, and keep recording the profile's full path; verify a fixture asserts every chapter-index row and every keyword-map row for the active catalog is present in the prepared context.
- [x] 3.3 Add a diagnostic that distinguishes "no book selected" from "book selected but sections unmatched" (e.g., `selection_failed` plus candidate count) and surface it alongside candidates; verify a caller can tell the two cases apart without inspecting an empty `books` array.

## 4. Skill workflow and rationale recording

- [x] 4.1 Accept an optional `selection_rationale` string in the request and copy it into the analysis manifest and operation receipt; verify it appears in diagnostics for candidate-based retries.
- [x] 4.2 Update book-user guidance with the two-phase workflow (query → candidates → explicit `book` → profile review → optional explicit `chapters`), including when to ask the user versus choose directly, and the requirement to record rationale on every retry.

## 5. Tests and evaluation gates

- [x] 5.1 Add deterministic fixtures for candidates-on-failure, explicit `book` then `chapters` flows, unknown-chapter failure with the available list, bidirectional keyword hits, and rationale propagation; verify expected manifests in unit and integration tests.
- [x] 5.2 Extend book-user behavioral evaluations: reproduced Chinese queries must not produce bare errors, candidate-based retries must show a recorded rationale, and chosen books must come from the offered candidates; verify deliberately broken fixtures fail each gate.
- [x] 5.3 Run the full test suite, `doctor --strict`, and the fixed evaluation suite; verify warm preparation remains within the 300ms budget and existing analysis fixtures pass unchanged.

## Verification record

- Full suite: 47 tests, 0 failures, 0 errors (interpreter: the repository's Python 3.14 with `fsrs==6.3.2`; the analysis suite is now part of `check_all.py` step 8).
- `check_all.py`: 39 checks passed, 0 failed. `booksys doctor --strict`: `status: ok`, 2 package manifests.
- Eval suite: report `passed: true`; 5 selection probes × 7 checks all pass.
- Negative controls (each gate broken on purpose, then reverted): guidance marker removed, candidates emptied, rationale stripped, selector made lenient, zero-tolerance set mismatched — every one turns the report red.
- Performance: failure path 18 ms; full query → book → chapters flow 34 ms wall; warm `prepare` stays under the 300 ms test budget.
- Candidates payload: 1840 bytes for the active 2-book catalog (920 bytes/book with chapter names, 340 bytes/book without, ~37 bytes per chapter-name entry).

## Follow-ups not part of this change

- `_write_context_file` previously measured its budget against the runtime root instead of the operation's `context` directory, so any caller-supplied `context_budget_bytes` silently suppressed writes. Fixed here because the new context sections depend on honoring that budget; the per-operation accounting now uses `_context_root`.
- Chapter `导言` (聪明投资者的 `00-本书的目的`) remains unreachable through the keyword map; explicit `chapters` (`["00"]`) is now the supported way to load it. Extending the resolver to map 导言 is still optional and out of scope.
