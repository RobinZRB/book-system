## ADDED Requirements

### Requirement: Active runtime content is authoritative
The runtime SHALL resolve books, chapters, facts, learning events, and generated projections from the active stage selected by `.booksys/current.json`.

#### Scenario: Prepare analysis from active content
- **WHEN** a user prepares an analysis request
- **THEN** selection and evidence loading use manifests and resources from the active stage

#### Scenario: Active stage is available
- **WHEN** the active stage contains valid packages
- **THEN** strict health checks and representative read/write operations succeed

### Requirement: Runtime uses one canonical v2 layout
The release SHALL provide one canonical v2 package catalog, event store, command surface, and runtime metadata layout selected by the active-stage pointer.

#### Scenario: Runtime command is invoked
- **WHEN** an operator invokes a supported runtime command
- **THEN** the command resolves the active stage and canonical runtime layout

#### Scenario: Runtime content is inspected
- **WHEN** source, active runtime data, skill bundles, evaluation assets, and operator documentation are inspected
- **THEN** each active reference describes the canonical v2 layout

## REMOVED Requirements

### Requirement: Active v2 content is authoritative
**Reason**: The replacement requirement states the active runtime contract without transition vocabulary.
**Migration**: Use `Active runtime content is authoritative`.

### Requirement: Compatibility paths are removed
**Reason**: The replacement requirement describes the canonical runtime layout directly.
**Migration**: Use `Runtime uses one canonical v2 layout`.
