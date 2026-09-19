## MODIFIED Requirements

### Requirement: Skill behavior evaluation gates
Each skill SHALL have representative behavioral evaluations that compare the changed skill against its accepted baseline. Releases SHALL treat fabrication, spoiler leakage, unauthorized writes, premature quiz feedback, mutable EMT expectations, and unsupported claims as zero-tolerance failures. The book-user evaluation suite SHALL include deterministic analysis-context fixtures and behavioral checks for protocol coverage, evidence traceability, insufficient-evidence reporting, external-fact provenance and missing-field disclosure, context-size budget, and preparation latency.

#### Scenario: Hard constraint regression
- **WHEN** a candidate skill violates any zero-tolerance behavior in an evaluation
- **THEN** the release gate fails even if mechanical unit tests pass

#### Scenario: Quality comparison
- **WHEN** hard constraints pass
- **THEN** the evaluation reports task success, traceability, context usage, latency, and blind quality comparison without requiring every soft metric to improve

#### Scenario: Book-user context regression
- **WHEN** the fixed stock-analysis fixture suite is evaluated
- **THEN** it verifies the selected protocol, each applicable protocol section's executed and matched/unmatched status, citation-capable book evidence, diagnostic fields, and configured latency and context-size budgets
