## ADDED Requirements

### Requirement: System and runtime roots are explicit
The system SHALL resolve executable assets from the project system root and runtime data from the project-local `.booksys` root by default or from an explicitly configured data root.

#### Scenario: Runtime root
- **WHEN** the project starts
- **THEN** runtime operations, events, projections, and receipts resolve under the runtime root and active content resolves through the current pointer

#### Scenario: Explicit external data root
- **WHEN** a user configures an external `data_root`
- **THEN** all book, reading, mastery, event, staging, and projection paths resolve beneath that root while skills, schemas, templates, and executable code remain beneath `system_root`

#### Scenario: Missing active pointer
- **WHEN** the active pointer or its stage is missing
- **THEN** startup fails with an actionable configuration error

### Requirement: Provide a supported command surface
The command-line interface SHALL expose the supported operations documented by its command help and package valid manifests for the active runtime.

#### Scenario: Supported command discovery
- **WHEN** an operator requests command help
- **THEN** the CLI lists the supported operations and their arguments

#### Scenario: Package import
- **WHEN** an operator imports a valid prepared package
- **THEN** the CLI publishes it into the active runtime stage

## REMOVED Requirements

### Requirement: Separate system and data roots
**Reason**: The replacement requirement states the canonical root contract without transition vocabulary.
**Migration**: Use `System and runtime roots are explicit`.

### Requirement: Provide a v2-only command surface
**Reason**: The replacement requirement describes the supported interface directly.
**Migration**: Use `Provide a supported command surface`.
