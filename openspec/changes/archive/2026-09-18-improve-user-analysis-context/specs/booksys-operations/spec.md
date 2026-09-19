## MODIFIED Requirements

### Requirement: Prepare an operation workspace
The system SHALL expose concrete preparation intents for reader, user, coach, and trainer workflows. Preparation SHALL produce a versioned operation workspace containing the normalized request, only the context required for that intent, result instructions, a strict result schema when a commit is permitted, and a snapshot of relevant input identities. For `user.analyze`, preparation SHALL select the applicable book or books and protocol, construct an evidence package from the book profile and every matched chapter resource without a default context-size ceiling, and return a machine-readable execution report. A read-only analysis workspace MUST NOT contain a result schema, result/commit instructions, or another writable-result contract.

#### Scenario: Prepare a chapter extraction
- **WHEN** `book-reader` prepares an extraction for a known book and chapter
- **THEN** the workspace contains the raw source, applicable extraction guidance, identifiers, provenance requirements, and result schema without requiring the skill to discover project paths

#### Scenario: Prepare a read-only analysis
- **WHEN** `book-user` prepares an analysis request
- **THEN** the workspace contains the selected protocol and minimum relevant evidence package and does not expose a writable result contract

#### Scenario: Analysis context audit
- **WHEN** a uniquely selected analysis request has indexed evidence
- **THEN** preparation includes every matched protocol section/chapter/resource without a default context-size ceiling, reports elapsed time and actual context size, and records evidence counts and skipped sections

#### Scenario: Insufficient evidence
- **WHEN** indexed selection cannot supply sufficient evidence for one or more applicable protocol sections
- **THEN** preparation returns an `insufficient_evidence` diagnostic with query terms, every matched chapter/resource, missing sections, and an explicit whole-book-search option without silently widening the search; matched evidence remains available for partial analysis

#### Scenario: Explicit whole-book search
- **WHEN** a caller explicitly requests whole-book search after an insufficient-evidence result
- **THEN** preparation performs the expanded search under its separately reported budget and returns the scope, elapsed time, context size, and resulting evidence coverage

#### Scenario: External facts are incomplete
- **WHEN** an analysis request includes external facts with missing source, retrieval time, applicable date, or field value
- **THEN** preparation preserves each missing item in the execution report and marks it unverified rather than treating it as book-derived or validated evidence

#### Scenario: External fact conflict
- **WHEN** an analysis request contains conflicting external facts for the same field and applicable date
- **THEN** preparation exposes the conflict diagnostic and does not collapse the values into one asserted fact

#### Scenario: Partial investment evidence
- **WHEN** an investment analysis has matched evidence but some protocol sections or external facts are unavailable
- **THEN** preparation retains the matched evidence and records the unavailable sections and facts as explicit states rather than suppressing the analysis

#### Scenario: Ambiguous selector
- **WHEN** a request matches more than one book, chapter, or concept
- **THEN** preparation fails with structured candidates and does not guess a target
