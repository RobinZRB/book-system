## MODIFIED Requirements

### Requirement: Separate system and data roots
The system SHALL resolve executable assets from the project system root and v2 runtime data from the project-local `.booksys` root by default or from an explicitly configured data root. It SHALL not expose a compatibility-default mode or activate a legacy workspace layout.

#### Scenario: V2 runtime root
- **WHEN** the project starts after cutover
- **THEN** runtime operations, events, projections, and receipts resolve under the v2 runtime root and active content resolves through the current v2 pointer

#### Scenario: Explicit external data root
- **WHEN** a user configures an external `data_root`
- **THEN** all book, reading, mastery, event, staging, and projection paths resolve beneath that root while skills, schemas, templates, and executable code remain beneath `system_root`

#### Scenario: Missing v2 pointer
- **WHEN** the active v2 pointer or stage is missing
- **THEN** startup fails with an actionable configuration error instead of falling back to legacy directories

#### Scenario: Missing active pointer
- **WHEN** the active pointer or its stage is missing
- **THEN** startup fails with an actionable configuration error

## ADDED Requirements

### Requirement: Provide a v2-only command surface
The command-line interface SHALL expose only supported v2 operations and SHALL not provide a baseline generator or a command that emits v1-labelled manifests.

#### Scenario: Removed baseline command
- **WHEN** an operator requests the former baseline command
- **THEN** command parsing rejects it without writing files
