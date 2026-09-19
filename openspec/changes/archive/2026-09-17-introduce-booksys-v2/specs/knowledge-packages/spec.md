## Purpose

Define portable, versioned, and strictly verifiable book knowledge packages whose machine-readable facts remain traceable to immutable raw sources while preserving useful Markdown views for people and AI.

## ADDED Requirements

### Requirement: Versioned package manifest
Each formal book SHALL have a package manifest declaring its schema version, immutable book identity, human-readable aliases, classification, generator metadata, and every authoritative or projected resource with its role, media type, byte size, and SHA-256 digest.

#### Scenario: Valid package manifest
- **WHEN** a package is validated
- **THEN** every declared authoritative resource exists, matches its digest and declared role, and conforms to the schema version named by the manifest

#### Scenario: Category changes
- **WHEN** a book is reclassified
- **THEN** its immutable identity and learning history remain unchanged while only its category attribute, aliases, and projections are updated

### Requirement: Stable identities and aliases
Books, chapters, concepts, relations, and claims SHALL have immutable internal identifiers. Human-readable names and slugs SHALL be stored as display values or aliases and SHALL not be used as the sole join key for learning history.

#### Scenario: Concept rename
- **WHEN** a concept display name changes
- **THEN** existing review events continue to resolve through the unchanged concept identifier and the previous name can remain as an alias

#### Scenario: Duplicate display names
- **WHEN** two concepts share the same display name
- **THEN** the system preserves distinct identifiers and requires contextual disambiguation instead of merging their history

### Requirement: Structured and narrative resource split
Concepts and relations SHALL be authoritative structured resources. Narrative reference material and non-spoiler chapter guidance SHALL remain Markdown authoritative content. Registries, concept-name indexes, glossaries, and human learning views SHALL be deterministic projections.

#### Scenario: Rebuild derived resources
- **WHEN** every derived resource for a valid book is deleted
- **THEN** the system can recreate byte-stable projections from authoritative resources without consulting prior projections

#### Scenario: Manual projection edit
- **WHEN** a generated projection is edited manually
- **THEN** strict validation reports drift and does not import the edit as an authoritative fact

### Requirement: Source provenance
Every structured concept, relation, evidence item, and claim SHALL identify the raw source digest and a verifiable character span. Page locators MAY be included when reliable, and evidence SHALL distinguish explicit source statements from inference or synthesis.

#### Scenario: Verifiable source span
- **WHEN** a structured fact references a raw-text span
- **THEN** the span resolves within the raw resource whose SHA-256 matches the recorded digest

#### Scenario: Unsupported claim
- **WHEN** a claim has no valid source span and is not explicitly classified as inference or synthesis with supporting references
- **THEN** strict validation rejects the package

### Requirement: Strict package validation
Strict validation SHALL fail on missing or empty core resources, malformed schemas, invalid identities, unresolved references, omitted indexed chapters, duplicate identifiers, invalid provenance, and projection drift. Legacy tolerance SHALL require an explicit compatibility mode and SHALL never hide configuration parse errors.

#### Scenario: Missing chapter guide
- **WHEN** a formal v2 chapter lacks its required non-spoiler guide
- **THEN** strict validation fails and identifies the chapter and missing role

#### Scenario: Invalid configuration
- **WHEN** configuration exists but cannot be parsed or contains an invalid required value
- **THEN** the command exits with failure rather than silently using default paths

### Requirement: Full staged legacy migration
The system SHALL migrate all existing formal books through a repeatable staged process that assigns stable identities, generates structured resources and manifests, renders legacy-compatible Markdown, and compares observable legacy content before cutover.

#### Scenario: Migration preview
- **WHEN** migration is planned
- **THEN** the system reports intended identifiers, unresolved references, missing provenance, projection differences, and a deterministic plan digest without modifying production data

#### Scenario: Atomic cutover
- **WHEN** a reviewed migration plan passes strict validation and parity checks
- **THEN** the new package set becomes authoritative atomically and the prior data remains available for the rollback window

