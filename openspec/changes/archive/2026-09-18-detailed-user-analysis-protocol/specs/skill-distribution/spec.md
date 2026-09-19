## MODIFIED Requirements

### Requirement: Skill behavior evaluation gates
Each skill SHALL have representative behavioral evaluations that compare the changed skill against its accepted baseline. Releases SHALL treat fabrication, spoiler leakage, unauthorized writes, premature quiz feedback, mutable EMT expectations, and unsupported claims as zero-tolerance failures.  Investment-analysis evaluations SHALL additionally reject an answer that omits the required Gate disposition, leaves a triggered risk without a disposition, omits an applicable protocol-dimension state, or hides missing/unverified external facts.

#### Scenario: Hard constraint regression
- **WHEN** a candidate skill violates any zero-tolerance behavior in an evaluation
- **THEN** the release gate fails even if mechanical unit tests pass

#### Scenario: Detailed investment analysis regression
- **WHEN** a candidate book-user response to an investment request omits a required Gate, risk disposition, dimension state, or missing-fact disclosure
- **THEN** the behavioral evaluation fails with the omitted contract element identified

#### Scenario: Quality comparison
- **WHEN** hard constraints pass
- **THEN** the evaluation reports task success, traceability, context usage, latency, and blind quality comparison without requiring every soft metric to improve
