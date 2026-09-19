## Purpose

Provide a small, deterministic operation interface that lets AI skills request prepared context and safely commit structured results without knowing storage paths, file formats, projection order, or recovery procedures.

## ADDED Requirements

### Requirement: Separate system and data roots
The system SHALL resolve a read-only `system_root` for executable assets and a writable `data_root` for private book and learner data. It SHALL retain the current in-project data layout as a compatibility default for one migration cycle, and SHALL reject configurations where the resolved roots violate their declared write policy.

#### Scenario: Explicit external data root
- **WHEN** a user configures an external `data_root`
- **THEN** all book, reading, mastery, event, staging, and projection paths resolve beneath that root while skills, schemas, templates, and executable code remain beneath `system_root`

#### Scenario: Legacy default layout
- **WHEN** no external `data_root` is configured during the compatibility cycle
- **THEN** the system uses the current project-local data directories and reports that the compatibility default is active

### Requirement: Prepare an operation workspace
The system SHALL expose concrete preparation intents for reader, user, coach, and trainer workflows. Preparation SHALL produce a versioned operation workspace containing the normalized request, only the context required for that intent, result instructions, a strict result schema when a commit is permitted, and a snapshot of relevant input identities.

#### Scenario: Prepare a chapter extraction
- **WHEN** `book-reader` prepares an extraction for a known book and chapter
- **THEN** the workspace contains the raw source, applicable extraction guidance, identifiers, provenance requirements, and result schema without requiring the skill to discover project paths

#### Scenario: Prepare a read-only analysis
- **WHEN** `book-user` prepares an analysis request
- **THEN** the workspace contains the selected protocol and minimum relevant evidence package and does not expose a writable result contract

#### Scenario: Ambiguous selector
- **WHEN** a request matches more than one book, chapter, or concept
- **THEN** preparation fails with structured candidates and does not guess a target

### Requirement: Commit operations deterministically
The system SHALL commit only workspaces created by the preparation interface. Commit SHALL validate the result schema, stable identities, provenance, current input snapshot, and domain invariants before changing authoritative data. Repeating an identical commit SHALL be idempotent, and a conflicting reuse of the same operation identity SHALL fail.

#### Scenario: Successful commit
- **WHEN** a valid unmodified workspace result is committed
- **THEN** authoritative data and all required projections become observable at one new logical revision and the command returns a structured receipt

#### Scenario: Stale workspace
- **WHEN** an input captured by the workspace has changed before commit
- **THEN** commit fails with a stale-operation diagnostic and leaves authoritative data unchanged

#### Scenario: Invalid result
- **WHEN** a result violates its schema or a domain invariant
- **THEN** commit fails before authoritative data is changed and reports each actionable violation

### Requirement: Provide read-only health checks
The system SHALL provide a strict `doctor` operation that validates configuration, package integrity, event integrity, references, scheduler compatibility, installations, and projection drift without changing files.

#### Scenario: Projection drift is detected without repair
- **WHEN** a generated Markdown projection differs from the deterministic rendering of its facts
- **THEN** `doctor` returns failure with the affected projection and performs no rewrite

#### Scenario: Explicit repair
- **WHEN** an operator explicitly invokes a projection write operation after reviewing diagnostics
- **THEN** only generated projections are replaced and authoritative facts remain unchanged

### Requirement: Preserve legacy entry points temporarily
The legacy pipeline script names and accepted arguments SHALL remain available for one compatibility cycle as adapters to the new operation interface. They SHALL not retain independent business logic or directly write legacy facts.

#### Scenario: Legacy script invocation
- **WHEN** a supported legacy command is invoked during the compatibility cycle
- **THEN** it translates the request to `booksys`, preserves documented success and failure behavior, and emits a deprecation diagnostic

#### Scenario: Compatibility removal gate
- **WHEN** all skills and checks use `booksys`, all data has migrated, and no legacy entry point has been observed for the declared compatibility cycle
- **THEN** a subsequent OpenSpec change may remove the adapters

