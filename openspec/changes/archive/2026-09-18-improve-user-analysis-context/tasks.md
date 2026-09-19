## 1. Analysis-context contract and selection

- [x] 1.1 Define and validate the typed `user.analyze` request and read-only manifest schema, including query, scope, external facts, status, coverage, budgets, and diagnostics; verify malformed and ambiguous requests return structured failures.
- [x] 1.2 Implement deterministic exact-book/category selection and stage-one scoring from the registry, profiles, glossary, and concept indexes; verify fixed fixtures select the expected books, protocol sections, candidates, scores, and rejection reasons.
- [x] 1.3 Implement bounded stage-two chapter evidence assembly with stable ordering, citation-capable excerpts, per-section execution states, and reserved profile/protocol/report capacity; verify the assembled fixture context stays within the configured size cap.
- [x] 1.4 Implement `insufficient_evidence` and explicit `whole_book` behavior without automatic expansion; verify missing coverage exposes the required diagnostic chain and explicit expansion reports its separate scope and budget.

## 2. Read-only workspace and skill integration

- [x] 2.1 Route `prepare user.analyze` through the analysis-context builder and write its protocol, profile, evidence package, manifest, and read-only consumption instructions; verify no result schema or commit instruction is present.
- [x] 2.2 Preserve external-fact provenance and missing fields in the manifest without inferring or merging them with book evidence; verify incomplete fixtures are marked unverified and remain visible.
- [x] 2.3 Replace book-user placeholder guidance with manifest-consumption and concise/expanded audit presentation rules; verify the bundle has no unresolved file reference and directs every applicable protocol section to an executed or unmatched result.
- [x] 2.4 Update public CLI output and error handling for the typed request and structured diagnostics; verify representative CLI requests are deterministic and expose operation path, status, and audit summary.

## 3. Quality and performance gates

- [x] 3.1 Add deterministic stock-analysis fixtures covering exact selection, category selection, no/weak evidence, protocol coverage, ambiguity, incomplete external facts, and explicit whole-book expansion; verify their expected manifests in unit tests.
- [x] 3.2 Add public integration tests for `user.analyze` workspaces, including selected protocol/evidence, read-only contract, traceability, and diagnostic completeness; verify the test suite catches the former empty-context regression.
- [x] 3.3 Add a local warm-run performance test and enforce the 300ms preparation target while recording actual context size; verify any caller-supplied context budget is honored.
- [x] 3.4 Extend the book-user behavioral evaluation gate to require protocol-section status, citation-capable evidence, missing-field disclosure, and no unsupported claims; verify a deliberately incomplete fixture fails the appropriate quality gate.

## 4. Verification and rollout

- [x] 4.1 Run the project health checks, full test suite, and fixed analysis regression/evaluation suite; verify all pass and record any environment-specific performance caveat.
- [x] 4.2 Review a representative ready, insufficient-evidence, and explicit whole-book manifest with the user-facing trace summaries; verify normal output remains concise and audit output expands only under the agreed conditions.

## 5. Partial analysis and no-ranking selection

- [x] 5.1 Change indexed selection to include every keyword-matched chapter/resource without relevance scoring or candidate eviction; verify the manifest exposes all matches and their trigger keywords.
- [x] 5.2 Allow partial analysis when coverage is incomplete, marking only unmatched protocol sections as unassessed; verify matched evidence remains available under `insufficient_evidence`.
- [x] 5.3 Update book-user guidance and regression tests for matched-evidence output, no-score diagnostics, and explicit whole-book expansion; verify Chinese/English mixed queries still pass the latency and context gates.
