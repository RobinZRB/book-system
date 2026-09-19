## MODIFIED Requirements

### Requirement: Full staged legacy migration
The migration output SHALL become the authoritative v2 package set after cutover, and legacy-compatible Markdown data SHALL no longer be required by runtime operations.

#### Scenario: Authoritative v2 package set
- **WHEN** the active stage passes strict manifest and provenance validation
- **THEN** runtime package selection reads only its manifests and resources

### Requirement: V2 package publication
The system SHALL provide a v2-only package importer that validates a prepared package's strict manifest and provenance and publishes it to the active stage without consulting legacy workspace directories.

#### Scenario: Authoritative v2 package set
- **WHEN** the active stage passes strict manifest and provenance validation
- **THEN** runtime package selection reads only its manifests and resources

#### Scenario: Publish a prepared package
- **WHEN** an operator imports a valid, uniquely named v2 package
- **THEN** it becomes available through the active package catalog and its manifest remains strict-valid

#### Scenario: Publish a package
- **WHEN** an operator imports a valid package with a unique path
- **THEN** it becomes available from the active stage

#### Scenario: Reject an existing package
- **WHEN** an import would overwrite an existing package
- **THEN** it fails without changing the active catalog
