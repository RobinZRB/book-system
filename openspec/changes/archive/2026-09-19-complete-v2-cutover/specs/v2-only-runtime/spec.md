## Purpose

Make the active v2 package and event store the sole authoritative runtime and remove the compatibility window once parity has been verified.

## MODIFIED Requirements

### Requirement: Active v2 content is authoritative
The runtime SHALL resolve books, chapters, facts, learning events, and generated projections from the active v2 stage selected by `.booksys/current.json`. It SHALL not fall back to legacy `books/`, `reading/`, or `mastery/` directories.

#### Scenario: Prepare analysis from v2 content
- **WHEN** a user prepares an analysis request
- **THEN** selection and evidence loading use v2 manifests and resources from the active stage

#### Scenario: Legacy content is absent
- **WHEN** legacy data directories are removed after cutover
- **THEN** strict health checks and representative read/write operations remain successful

### Requirement: Compatibility paths are removed
The release SHALL remove rollback metadata, legacy pipeline adapters, legacy-only CLI actions, and historical migration snapshots after the active stage passes verification.

#### Scenario: Rollback is unavailable after cutover
- **WHEN** an operator requests a removed compatibility action
- **THEN** the CLI reports that the project is v2-only and does not recreate or consult legacy state

#### Scenario: Removed command requested
- **WHEN** an operator requests a removed compatibility action
- **THEN** the CLI rejects it and does not recreate retired state
