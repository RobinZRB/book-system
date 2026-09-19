## ADDED Requirements

### Requirement: Direct catalog interface
The command surface SHALL let a skill list declared books and locate declared book, chapter, and concept resources by stable identifier. It SHALL return declared identities, locations, and resource paths, and SHALL reject an unknown identifier. It SHALL NOT match on a title, display name, or alias, SHALL NOT return candidates for the caller to choose from, and SHALL NOT infer semantic relevance from a user's question.

#### Scenario: Skill locates a selected chapter
- **WHEN** a skill asks for a declared book and chapter by identifier
- **THEN** the command returns direct source, guide, and concept paths without creating a workspace or copying files

#### Scenario: A display value is passed instead of an identifier
- **WHEN** a selector is a title, display name, or alias rather than a declared stable identifier
- **THEN** the command rejects it without guessing which entity was meant and without offering candidates

### Requirement: System and runtime roots are explicit
The system SHALL resolve executable assets from the project system root and private learning state from the project-local `.booksys` root by default or an explicitly configured data root. Declared book packages SHALL resolve from the canonical catalog beneath the system root and SHALL not require an active stage pointer.

#### Scenario: Runtime root
- **WHEN** the project starts
- **THEN** private learning events resolve beneath the runtime root and book resources resolve from the canonical direct catalog

#### Scenario: Explicit external data root
- **WHEN** a user configures an external `data_root`, through a command option or a hand-written `.booksys/config.json`
- **THEN** learning events and derived learning state resolve beneath that root while books, skill assets, schemas, templates, and executable code remain beneath `system_root`

#### Scenario: Missing catalog
- **WHEN** the canonical catalog is missing or malformed
- **THEN** a catalog command fails with an actionable configuration error

#### Scenario: Missing active pointer
- **WHEN** a legacy active pointer is absent
- **THEN** direct catalog and learning commands continue without consulting it

### Requirement: Provide read-only health checks
The system SHALL provide a `doctor` operation that validates direct catalog integrity, declared source, guide, and concept resources, and learning-event integrity without changing files. It SHALL not require analysis workspaces, receipts, generic projections, an installation target, or an adapter probe.

#### Scenario: Invalid declared resource
- **WHEN** a book declaration names a missing required resource
- **THEN** `doctor` returns failure identifying the book and resource without changing files

#### Scenario: Invalid learning event
- **WHEN** an event violates a learning invariant
- **THEN** `doctor` reports the affected event stream without repairing it

#### Scenario: Missing scheduler dependency at use time
- **WHEN** a review is requested but the pinned scheduler dependency is unavailable or incompatible
- **THEN** the review command fails explicitly and writes nothing

### Requirement: Provide a supported command surface
The command-line interface SHALL expose catalog lookup, learning state, package publication, and `doctor`. Ordinary question answering SHALL not require a generic operation identifier, prepared context, result file, commit receipt, or projection command. The surface SHALL not include an installation command, an archive-building command, or a configuration-writing command.

#### Scenario: Supported command discovery
- **WHEN** an operator requests command help
- **THEN** the CLI lists the supported catalog, learning, package, and health commands with their arguments

#### Scenario: Direct answer preparation
- **WHEN** a book-user skill needs book material for a question
- **THEN** it can discover and read declared resources through catalog commands without creating a persistent operation workspace

#### Scenario: Package import
- **WHEN** an operator imports a valid prepared small package
- **THEN** the CLI publishes it into the canonical direct catalog
