## 1. Structured detailed-analysis plan

- [x] 1.1 Extend `user.analyze` manifests with deterministic investment presentation mode, Gate, risk, dimension, counter-evidence, and missing-fact execution records; verify fixed preparation fixtures produce stable records without changing read-only behavior.
- [x] 1.2 Map matched and unmatched profile/protocol evidence conservatively into the plan, including explicit whole-book and partial-analysis states; verify unmatched evidence cannot become a passing or fabricated finding.

## 2. Book-user presentation contract

- [x] 2.1 Update bundled book-user guidance so investment/company/stock requests default to visible `Gate → 红旗调查 → 多维分析 → 反方证据 → 缺失项 → 结论与链路`, with every applicable status and citation shown; verify the bundle remains self-contained.
- [x] 2.2 Define concise-mode detection and its minimum retained disclosures; verify an explicit quick-scan request can be shorter without hiding material risks, evidence provenance, or missing facts.

## 3. Regression protection

- [x] 3.1 Add unit and integration tests for detailed-plan construction, Chinese/English investment queries, partial evidence, absent counter-evidence, and unverified external facts; verify all new assertions pass deterministically.
- [x] 3.2 Extend book-user behavioral evaluations to reject missing Gate, unresolved triggered risk, omitted dimension state, or hidden missing fact; verify a deliberately incomplete response fails with the named diagnostic.
- [x] 3.3 Run strict OpenSpec validation, project health checks, and the full test/evaluation suite; verify detailed preparation preserves the warm-run performance target and report measured results.
