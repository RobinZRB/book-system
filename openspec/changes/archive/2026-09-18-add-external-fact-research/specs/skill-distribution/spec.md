## MODIFIED Requirements

### Requirement: Four focused self-contained skills
The distribution SHALL retain separate `book-reader`, `book-user`, `book-coach`, and `book-trainer` skills. Each bundle SHALL contain its required instructions and referenced resources using skill-root-relative paths, and SHALL delegate deterministic storage and scheduling work to `booksys`. The book-user bundle SHALL derive a framework-driven research plan before orchestrating independent external-fact research, counter-evidence research, and final synthesis for investment/company analysis, while keeping every bundle usable with an explicit offline fallback.

#### Scenario: Skill activation
- **WHEN** one of the four skills is activated outside the source repository
- **THEN** it can load every required bundled instruction without following a path into a sibling project directory

#### Scenario: Investment analysis orchestration
- **WHEN** book-user receives an investment/company request and external research is available
- **THEN** it derives a visible plan from the selected framework, obtains only plan-linked structured research inputs before synthesis, and keeps book evidence, supporting external facts, counter-evidence, and inferences distinct in the final answer

#### Scenario: Offline fallback
- **WHEN** external research is unavailable
- **THEN** book-user discloses the unavailable fields and may continue with validated caller-supplied facts and book-only partial analysis

#### Scenario: Skill instruction scope
- **WHEN** a skill describes an executable workflow
- **THEN** it states when to trigger, the semantic decisions the AI owns, and the concrete `booksys` operation to invoke without duplicating storage layouts or projection procedures

### Requirement: Skill behavior evaluation gates
Each skill SHALL have representative behavioral evaluations that compare the changed skill against its accepted baseline. Releases SHALL treat fabrication, spoiler leakage, unauthorized writes, premature quiz feedback, mutable EMT expectations, and unsupported claims as zero-tolerance failures.  Book-user investment evaluations SHALL also treat missing external-fact provenance, silently resolved conflicts, unsupported source-tier claims, and omitted counter-evidence disclosure as zero-tolerance failures.

#### Scenario: Hard constraint regression
- **WHEN** a candidate skill violates any zero-tolerance behavior in an evaluation
- **THEN** the release gate fails even if mechanical unit tests pass

#### Scenario: External-fact provenance regression
- **WHEN** a candidate book-user response treats an unverified, stale, conflicting, or uncited external fact as settled evidence
- **THEN** the behavioral evaluation fails and identifies the provenance or conflict violation

#### Scenario: Quality comparison
- **WHEN** hard constraints pass
- **THEN** the evaluation reports task success, traceability, context usage, latency, and blind quality comparison without requiring every soft metric to improve
