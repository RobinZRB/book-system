## 1. Fact-package contract

- [x] 1.1 Derive and validate a research plan from selected protocol sections, Gate items, red flags, dimensions, and evidence gaps; verify every requested field has a framework link and unrelated fields are excluded.
- [x] 1.2 Define and validate the canonical external fact package, including subject, field, value, framework link, source identity, retrieval time, applicable date, source tier, verification state, and counter-evidence linkage; verify malformed or incomplete facts remain explicit diagnostics.
- [x] 1.3 Extend `user.analyze` preparation to preserve plan coverage, fact freshness, missing fields, and same-field/date conflicts without collapsing them; verify compatible legacy `external_facts` inputs remain accepted.

## 2. Research orchestration

- [x] 2.1 Update book-user guidance with the framework-driven research plan, two independent research roles, and synthesis reinjection sequence; verify neither research role can write package data, search unrelated fields, or produce the final investment conclusion.
- [x] 2.2 Define the source-tier selection rules, counter-evidence scope disclosure, and offline/caller-supplied fallback; verify unavailable research yields partial analysis rather than fabricated external facts.

## 3. Quality gates

- [x] 3.1 Add deterministic fixtures and tests for framework-plan coverage, primary facts, secondary market facts, missing facts, stale facts, conflicts, counter-evidence, and offline fallback; verify the prepared manifest exposes each state separately.
- [x] 3.2 Extend behavioral evaluations to fail uncited/unsupported external claims, silently resolved conflicts, and omitted counter-evidence disclosure; verify each deliberate regression produces its named failure.
- [x] 3.3 Run strict OpenSpec validation, health checks, full tests, and behavioral evaluations; verify the book-only preparation path retains its existing latency target and report research-orchestration timing separately.
