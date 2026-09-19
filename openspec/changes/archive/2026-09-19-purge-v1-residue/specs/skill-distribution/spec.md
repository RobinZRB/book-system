## MODIFIED Requirements

### Requirement: Skill behavior evaluation gates
Each skill SHALL have representative behavioral evaluations that compare the changed skill against its accepted baseline. Releases SHALL treat fabrication, spoiler leakage, unauthorized writes, premature quiz feedback, mutable EMT expectations, and unsupported claims as zero-tolerance failures. Book-user investment evaluations SHALL also treat missing external-fact provenance, silently resolved conflicts, unsupported source-tier claims, omitted counter-evidence disclosure, omitted Gate disposition, unresolved triggered risk, omitted protocol-dimension state, and hidden missing or unverified external facts as zero-tolerance failures. Evaluation manifests and reports SHALL use v2-native baseline identifiers.

#### Scenario: Hard constraint regression
- **WHEN** a candidate skill violates any zero-tolerance behavior in an evaluation
- **THEN** the release gate fails even if mechanical unit tests pass

#### Scenario: Quality comparison
- **WHEN** hard constraints pass
- **THEN** the evaluation reports task success, traceability, context usage, latency, and blind quality comparison without requiring every soft metric to improve

#### Scenario: Book-user context regression
- **WHEN** the fixed stock-analysis fixture suite is evaluated
- **THEN** it verifies the selected protocol, each applicable protocol section's executed and matched/unmatched status, citation-capable book evidence, diagnostic fields, and configured latency and context-size budgets

#### Scenario: Detailed investment analysis regression
- **WHEN** a candidate book-user response to an investment request omits a required Gate, risk disposition, dimension state, or missing-fact disclosure
- **THEN** the behavioral evaluation fails with the omitted contract element identified

#### Scenario: V2 evaluation identity
- **WHEN** behavioral evaluations or their reports are generated
- **THEN** they identify the accepted v2 baseline without a v1-labelled field or artifact
