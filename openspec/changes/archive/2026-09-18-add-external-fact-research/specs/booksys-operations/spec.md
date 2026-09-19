## MODIFIED Requirements

### Requirement: Prepare an operation workspace
The system SHALL expose concrete preparation intents for reader, user, coach, and trainer workflows. Preparation SHALL produce a versioned operation workspace containing the normalized request, only the context required for that intent, result instructions, a strict result schema when a commit is permitted, and a snapshot of relevant input identities.  A `book-user` investment analysis workspace SHALL accept a validated external fact package, retain its provenance, freshness, conflicts, counter-evidence, and missing-data diagnostics, and expose those records separately from book evidence without a writable result contract.

#### Scenario: Prepare a chapter extraction
- **WHEN** `book-reader` prepares an extraction for a known book and chapter
- **THEN** the workspace contains the raw source, applicable extraction guidance, identifiers, provenance requirements, and result schema without requiring the skill to discover project paths

#### Scenario: Prepare a read-only analysis
- **WHEN** `book-user` prepares an analysis request
- **THEN** the workspace contains the selected protocol, minimum relevant book evidence, validated external facts when supplied, and does not expose a writable result contract

#### Scenario: External fact conflict
- **WHEN** an analysis request contains conflicting external facts for the same field and applicable date
- **THEN** preparation exposes the conflict diagnostic and does not collapse the values into one asserted fact

#### Scenario: Ambiguous selector
- **WHEN** a request matches more than one book, chapter, or concept
- **THEN** preparation fails with structured candidates and does not guess a target
