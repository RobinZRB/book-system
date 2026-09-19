## MODIFIED Requirements

### Requirement: Four focused self-contained skills
Each skill SHALL load runtime guidance and protocol assets from its own `skills/` bundle and SHALL not require legacy project directories or pipeline scripts. Book-user guidance SHALL define a two-phase selection workflow: prepare with the raw query; on candidates, choose book(s) — asking the user when genuinely ambiguous — and retry with an explicit `book` selector; after reading the prepared profile, judge default chapter coverage and retry with explicit `chapters` when needed; and record a selection rationale on every candidate-based retry.

#### Scenario: Skill activation
- **WHEN** one of the four skills is activated outside the source repository
- **THEN** it can load every required bundled instruction without following a path into a sibling project directory

#### Scenario: Investment analysis orchestration
- **WHEN** book-user receives an investment/company request and external research is available
- **THEN** it derives a visible plan from the selected framework, obtains only plan-linked structured research inputs before synthesis, and keeps book evidence, supporting external facts, counter-evidence, and inferences distinct in the final answer

#### Scenario: Candidate-driven book selection
- **WHEN** an analysis request returns catalog candidates instead of a selected book
- **THEN** book-user chooses from the offered candidates (confirming with the user when genuinely ambiguous), retries with an explicit selector, and records its rationale

#### Scenario: Caller-selected chapters
- **WHEN** the prepared profile's default chapter candidates do not cover the user's question
- **THEN** book-user names explicit chapters from the profile's chapter index and retries preparation

#### Scenario: Offline fallback
- **WHEN** external research is unavailable
- **THEN** book-user discloses the unavailable fields and may continue with validated caller-supplied facts and book-only partial analysis

#### Scenario: Skill instruction scope
- **WHEN** a skill describes an executable workflow
- **THEN** it states when to trigger, the semantic decisions the AI owns, and the concrete `booksys` operation to invoke without duplicating storage layouts or projection procedures

#### Scenario: Legacy project directories are absent
- **WHEN** a skill is activated after v2 cutover
- **THEN** all guidance, protocol, and runtime references resolve inside the canonical skill bundle and v2 runtime

#### Scenario: Runtime path scan
- **WHEN** canonical skill documentation and configuration are scanned before cleanup
- **THEN** no executable instruction points to a removed top-level skill, data, or pipeline directory

### Requirement: Skill behavior evaluation gates
Each skill SHALL have representative behavioral evaluations that compare the changed skill against its accepted baseline. Releases SHALL treat fabrication, spoiler leakage, unauthorized writes, premature quiz feedback, mutable EMT expectations, and unsupported claims as zero-tolerance failures. Book-user investment evaluations SHALL also treat missing external-fact provenance, silently resolved conflicts, unsupported source-tier claims, omitted counter-evidence disclosure, omitted Gate disposition, unresolved triggered risk, omitted protocol-dimension state, and hidden missing or unverified external facts as zero-tolerance failures. Book-user selection evaluations SHALL treat bare selection errors on the reproduced Chinese failure queries, books chosen outside the offered candidates, and candidate-based retries without a recorded rationale as failures. Evaluation manifests and reports SHALL use v2-native baseline identifiers.

#### Scenario: Hard constraint regression
- **WHEN** a candidate skill violates any zero-tolerance behavior in an evaluation
- **THEN** the release gate fails even if mechanical unit tests pass

#### Scenario: Quality comparison
- **WHEN** hard constraints pass
- **THEN** the evaluation reports task success, traceability, context usage, latency, and blind quality comparison without requiring every soft metric to improve

#### Scenario: Book-user context regression
- **WHEN** the fixed stock-analysis fixture suite is evaluated
- **THEN** it verifies the selected protocol, each applicable protocol section's executed and matched/unmatched status, citation-capable book evidence, diagnostic fields, and configured latency and context-size budgets

#### Scenario: Chinese-query selection regression
- **WHEN** the reproduced failure queries (company names without domain words, book core keywords) are evaluated
- **THEN** the result contains structured candidates or a correctly chosen book with a recorded rationale, never a bare error

#### Scenario: Detailed investment analysis regression
- **WHEN** a candidate book-user response to an investment request omits a required Gate, risk disposition, dimension state, or missing-fact disclosure
- **THEN** the behavioral evaluation fails with the omitted contract element identified

#### Scenario: V2 evaluation identity
- **WHEN** behavioral evaluations or their reports are generated
- **THEN** they identify the accepted v2 baseline without a v1-labelled field or artifact
