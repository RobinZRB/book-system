## MODIFIED Requirements

### Requirement: Separate system and data roots
The system SHALL resolve executable assets from the project system root and runtime data from the v2 runtime root. It SHALL not activate the project-local legacy compatibility default.

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
